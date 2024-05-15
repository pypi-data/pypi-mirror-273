import os, re 
import math, time
import shutil, random
import secrets, hashlib
import logging, binascii
import requests, tempfile
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.PublicKey import RSA
from .errors import ValidationError, RequestError
from .crypto import make_id, mpi_to_int, modular_inverse
from .crypto import decrypt_key, stringhash, prepare_key
from .crypto import a32_to_base64, encrypt_key, base64_url_encode
from .crypto import encrypt_attr, base64_to_a32, base64_url_decode
from .crypto import decrypt_attr, a32_to_str, get_chunks, str_to_a32
from tenacity import retry, wait_exponential, retry_if_exception_type
#===================================================================================================================================
logger = logging.getLogger(__name__)

class Mega:

    def __init__(self):
        self.sid = None
        self.timeout = 160
        self.schema = 'https'
        self.domain = 'mega.nz'
        self.request_id = make_id(10)
        self.trash_folders_uid = None
        self.api_domain = 'mega.co.nz'
        self.sequence_num = random.randint(0, 0xFFFFFFFF)

#===================================================================================================================================

    def _init_shared_keys(self, files, shared_keys):
        ok_dict = {}
        for ok_item in files['ok']:
            shared_key = decrypt_key(base64_to_a32(ok_item['k']),
                                     self.master_key)
            ok_dict[ok_item['h']] = shared_key
        for s_item in files['s']:
            if s_item['u'] not in shared_keys:
                shared_keys[s_item['u']] = {}
            if s_item['h'] in ok_dict:
                shared_keys[s_item['u']][s_item['h']] = ok_dict[s_item['h']]
    
        self.shared_keys = shared_keys

#===================================================================================================================================

    def get_files(self):
        files = self.api_request({'a': 'f', 'c': 1, 'r': 1})
        files_dict = {}
        shared_keys = {}
        self._init_shared_keys(files, shared_keys)
        for file in files['f']:
            processed_file = self.process_file(file, shared_keys)
            if processed_file['a']:
                files_dict[file['h']] = processed_file
        return files_dict
    
#===================================================================================================================================

    def get_node_by_type(self, type):
        nodes = self.get_files()
        for node in list(nodes.items()):
            if node[1]['t'] == type:
                return node

#===================================================================================================================================

    def process_file(self, file, shared_keys):
        if file['t'] == 0 or file['t'] == 1:
            key = None
            keys = dict(keypart.split(':', 1) for keypart in file['k'].split('/') if ':' in keypart)
            uid = file['u']
            if uid in keys:
                key = decrypt_key(base64_to_a32(keys[uid]), self.master_key)
            elif 'su' in file and 'sk' in file and ':' in file['k']:
                shared_key = decrypt_key(base64_to_a32(file['sk']), self.master_key)
                key = decrypt_key(base64_to_a32(keys[file['h']]), shared_key)
                if file['su'] not in shared_keys:
                    shared_keys[file['su']] = {}
                shared_keys[file['su']][file['h']] = shared_key
            elif file['u'] and file['u'] in shared_keys:
                for hkey in shared_keys[file['u']]:
                    shared_key = shared_keys[file['u']][hkey]
                    if hkey in keys:
                        key = keys[hkey]
                        key = decrypt_key(base64_to_a32(key), shared_key)
                        break
            if file['h'] and file['h'] in shared_keys.get('EXP', ()):
                shared_key = shared_keys['EXP'][file['h']]
                encrypted_key = str_to_a32(base64_url_decode(file['k'].split(':')[-1]))
                key = decrypt_key(encrypted_key, shared_key)
                file['shared_folder_key'] = shared_key
            if key is not None:
                if file['t'] == 0:
                    k = (key[0] ^ key[4], key[1] ^ key[5], key[2] ^ key[6], key[3] ^ key[7])
                    file['iv'] = key[4:6] + (0, 0)
                    file['meta_mac'] = key[6:8]
                else:
                    k = key
                file['key'] = key
                file['k'] = k
                attributes = base64_url_decode(file['a'])
                attributes = decrypt_attr(attributes, k)
                file['a'] = attributes
            elif file['k'] == '':
                file['a'] = False
        elif file['t'] == 2:
            self.root_id = file['h']
            file['a'] = {'n': 'Cloud Drive'}
        elif file['t'] == 3:
            self.inbox_id = file['h']
            file['a'] = {'n': 'Inbox'}
        elif file['t'] == 4:
            self.trashbin_id = file['h']
            file['a'] = {'n': 'Rubbish Bin'}
    
        return file

#===================================================================================================================================

    def login_process(self, resp, password):
        encrypted_master_key = base64_to_a32(resp['k'])
        self.master_key = decrypt_key(encrypted_master_key, password)
        if 'tsid' in resp:
            tsid = base64_url_decode(resp['tsid'])
            key_encrypted = a32_to_str(encrypt_key(str_to_a32(tsid[:16]), self.master_key))
            if key_encrypted == tsid[-16:]:
                self.sid = resp['tsid']
        elif 'csid' in resp:
            encrypted_rsa_private_key = base64_to_a32(resp['privk'])
            rsa_private_key = decrypt_key(encrypted_rsa_private_key, self.master_key)
            private_key = a32_to_str(rsa_private_key)
            rsa_private_key = [0, 0, 0, 0]
            for i in range(4):
                bitlength = (private_key[0] * 256) + private_key[1]
                bytelength = math.ceil(bitlength / 8)
                bytelength += 2
                rsa_private_key[i] = mpi_to_int(private_key[:bytelength])
                private_key = private_key[bytelength:]
            first_factor_p = rsa_private_key[0]
            second_factor_q = rsa_private_key[1]
            private_exponent_d = rsa_private_key[2]
            rsa_modulus_n = first_factor_p * second_factor_q
            phi = (first_factor_p - 1) * (second_factor_q - 1)
            public_exponent_e = modular_inverse(private_exponent_d, phi)
            rsa_components = (rsa_modulus_n, public_exponent_e, private_exponent_d, first_factor_p, second_factor_q)
            rsa_decrypter = RSA.construct(rsa_components)
            encrypted_sid = mpi_to_int(base64_url_decode(resp['csid']))
            sid = '%x' % rsa_decrypter._decrypt(encrypted_sid)
            sid = binascii.unhexlify('0' + sid if len(sid) % 2 else sid)
            self.sid = base64_url_encode(sid[:43])

#===================================================================================================================================

    def login_anonymous(self):
        master_key = [random.randint(0, 0xFFFFFFFF)] * 4
        password_key = [random.randint(0, 0xFFFFFFFF)] * 4
        session_self_challenge = [random.randint(0, 0xFFFFFFFF)] * 4

        user = self.api_request( {'a': 'up', 'k': a32_to_base64(encrypt_key(master_key, password_key)),
                                  'ts': base64_url_encode(a32_to_str(session_self_challenge) + 
                                                          a32_to_str(encrypt_key(session_self_challenge, master_key)))} )

        resp = self.api_request({'a': 'us', 'user': user})
        if isinstance(resp, int):
            raise RequestError(resp)
        self.login_process(resp, password_key)

#===================================================================================================================================

    def login(self, email=None, password=None):
        self.login_anonymous()
        self.trash_folders_uid = self.get_node_by_type(4)[0]
        return self

#===================================================================================================================================

    async def display(self, stime, tsize, dsize, message, progress):
        if message and progress:
            await progress(stime, tsize, dsize, message)
        elif progress:
            await progress(stime, tsize, dsize)
        else: pass

#===================================================================================================================================

    @retry(retry=retry_if_exception_type(RuntimeError), wait=wait_exponential(multiplier=2, min=2, max=60))
    def api_request(self, data):

        params = {'id': self.sequence_num}
        self.sequence_num += 1
        if self.sid:
            params.update({'sid': self.sid})
        if not isinstance(data, list):
            data = [data]

        url = f'{self.schema}://g.api.{self.api_domain}/cs'
        response = requests.post(url, params=params, json=data, timeout=self.timeout)
        json_resp = response.json()
        try:
            if isinstance(json_resp, list):
                int_resp = json_resp[0] if isinstance(json_resp[0], int) else None
            elif isinstance(json_resp, int):
                int_resp = json_resp
        except IndexError:
            int_resp = None
        if int_resp is not None:
            if int_resp == 0:
                return int_resp
            if int_resp == -3:
                msg = 'Request failed, retrying'
                logger.info(msg)
                raise RuntimeError(msg)
            raise RequestError(int_resp)
        return json_resp[0]

#===================================================================================================================================

    async def ismega_link(self, url: str):
        return url.startswith(f'{self.schema}://{self.domain}') or url.startswith(f'{self.schema}://{self.api_domain}')

#===================================================================================================================================

    async def follow_redirects(self, url: str):
        for i in range(10):
            if await self.ismega_link(url):
                return url
            resp = requests.get(url, allow_redirects=False)
            if resp.is_redirect or resp.is_permanent_redirect:
                url = resp.headers['Location']
                continue
            else:
                raise RuntimeError('Url is not a redirect nor a mega link')
        raise RuntimeError('Too many redirects')

#===================================================================================================================================

    async def parse_uri(self, url: str):
        url = await self.follow_redirects(url)
        if '/file/' in url:
            url = url.replace(' ', '')
            file_id = re.findall(r'\W\w\w\w\w\w\w\w\w\W', url)[0][1:-1]
            id_index = re.search(file_id, url).end()
            key = url[id_index + 1:]
            return f'{file_id}!{key}'.split('!')
        elif '!' in url:
            match = re.findall(r'/#!(.*)', url)
            path = match[0]
            return path.split('!')
        else:
            raise RequestError('Url key missing')

#===================================================================================================================================

    async def download(self, url, message=None, progress=None, dest_path=None, dest_filename=None):
        path_mid = await self.parse_uri(url)
        file_uid = path_mid[0]
        file_key = path_mid[1]
        return await self.downloadR(file_uid, file_key, message=message, progress=progress,
                               is_public=True, dest_path=dest_path, dest_filename=dest_filename)

#===================================================================================================================================

    async def modchunked(self, chunk):
        modchunk = len(chunk) % 16
        if modchunk == 0:
            modchunk = 16
            last_block = chunk[-modchunk:]
            return modchunk, last_block
        else:
            last_block = chunk[-modchunk:] + (b'\0' * (16 - modchunk))
            return modchunk, last_block

#===================================================================================================================================

    async def downloadR(self, file_uid, file_key, message, progress,
                  file=None, dest_path=None, dest_filename=None, is_public=False):
    
        stime = time.time()
        if file == None:
            file_key = base64_to_a32(file_key) if is_public else file_key
            file_data = self.api_request({'a': 'g', 'g': 1, 'p' if is_public else 'n': file_uid})
            k = (file_key[0] ^ file_key[4], file_key[1] ^ file_key[5], file_key[2] ^ file_key[6], file_key[3] ^ file_key[7])
            iv = file_key[4:6] + (0, 0)
            meta_mac = file_key[6:8]
        else:
            file_data = self.api_request({'a': 'g', 'g': 1, 'n': file['h']})
            k = file['k']
            iv = file['iv']
            meta_mac = file['meta_mac']

        if 'g' not in file_data:
            raise RequestError('File not accessible anymore')

        tsize = file_data['s']
        file_url = file_data['g']
        attribs = base64_url_decode(file_data['at'])
        attribs = decrypt_attr(attribs, k)
        input_file = requests.get(file_url, stream=True).raw
        dest_patho = '' if dest_path == None else dest_path + '/'
        file_name = dest_filename if dest_filename != None else attribs['n']
        output_path = Path(dest_patho + file_name)
        with tempfile.NamedTemporaryFile(mode='w+b', prefix='megapy_', delete=False) as tlocation:
            k_str = a32_to_str(k)
            mac_bytes = b'\0' * 16
            counter = Counter.new(128, initial_value=((iv[0] << 32) + iv[1]) << 64)
            aes = AES.new(k_str, AES.MODE_CTR, counter=counter)
            mac_encryptor = AES.new(k_str, AES.MODE_CBC, mac_bytes)
            iv_str = a32_to_str([iv[0], iv[1], iv[0], iv[1]])
            for chunk_start, chunk_size in get_chunks(tsize):
                chunk = input_file.read(chunk_size)
                chunk = aes.decrypt(chunk)
                tlocation.write(chunk)
                await self.display(stime, tsize, len(chunk), message, progress)
                encryptor = AES.new(k_str, AES.MODE_CBC, iv_str)
                mv = memoryview(chunk)
                modchunk, last_block = await self.modchunked(chunk)
                rest_of_chunk = mv[:-modchunk]
                encryptor.encrypt(rest_of_chunk)
                input_to_mac = encryptor.encrypt(last_block)
                mac_bytes = mac_encryptor.encrypt(input_to_mac)

            file_mac = str_to_a32(mac_bytes)
            if (file_mac[0] ^ file_mac[1], file_mac[2] ^ file_mac[3]) != meta_mac:
                raise ValueError('Mismatched mac')
        
            output_name = tlocation.name
            tlocation.close()
            shutil.move(output_name, output_path)
            return output_path

#===================================================================================================================================
    
    async def getinfo(self, url):
        fileuid, filekey = await self.parse_uri(url)
        return await self.exeinfo(fileuid, filekey)

#===================================================================================================================================

    async def exeinfo(self, file_uid, file_key):
        data = self.api_request({'a': 'g', 'p': file_uid, 'ssm': 1})
        if isinstance(data, int):
            raise RequestError(data)

        if 'at' not in data or 's' not in data:
            raise ValueError("Unexpected result", data)

        key = base64_to_a32(file_key)
        k = (key[0] ^ key[4], key[1] ^ key[5], key[2] ^ key[6], key[3] ^ key[7])
        unencrypted_attrs = decrypt_attr(base64_url_decode(data['at']), k)
        if not unencrypted_attrs:
            return None
            
        filesi = data['s']
        filena = unencrypted_attrs['n']
        moonus = {'fliesize': filesi, 'filename': filena}
        return moonus

#===================================================================================================================================
