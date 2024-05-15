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
        self.api_domain = 'mega.co.nz'
        self.sequence_num = random.randint(0, 0xFFFFFFFF)

#===================================================================================================================================

    async def display(self, stime, tsize, dsize, message, progress):
        if message and progress:
            progress(stime, tsize, dsize, message)
        elif progress:
            progress(stime, tsize, dsize)
        else: pass

#===================================================================================================================================

    @retry(retry=retry_if_exception_type(RuntimeError), wait=wait_exponential(multiplier=2, min=2, max=60))
    async def api_request(self, data):

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
            return f'{file_id}!{key}'
        elif '!' in url:
            match = re.findall(r'/#!(.*)', url)
            path = match[0]
            return path
        else:
            raise RequestError('Url key missing')

#===================================================================================================================================

    async def download(self, url, message=None, progress=None, dest_path=None, dest_filename=None):
        path_mid = await self.parse_uri(url).split('!')
        file_uid = path_mid[0]
        file_key = path_mid[1]
        return await self.downloadR(file_uid, file_key, message=message, progress=progress,
                               is_public=True, dest_path=dest_path, dest_filename=dest_filename)

#===================================================================================================================================
    
    async def downloadR(self, file_uid, file_key, message, progress,
                  file=None, dest_path=None, dest_filename=None, is_public=False):
    
        stime = time.time()
        if file == None:
            file_key = base64_to_a32(file_key) if is_public else file_key
            file_data = await self.api_request({'a': 'g', 'g': 1, 'p' if is_public else 'n': file_uid})
            k = (file_key[0] ^ file_key[4], file_key[1] ^ file_key[5], file_key[2] ^ file_key[6], file_key[3] ^ file_key[7])
            iv = file_key[4:6] + (0, 0)
            meta_mac = file_key[6:8]
        else:
            file_data = await self.api_request({'a': 'g', 'g': 1, 'n': file['h']})
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
                encryptor = AES.new(k_str, AES.MODE_CBC, iv_str)
                for i in range(0, len(chunk) - 16, 16):
                    block = chunk[ i : i + 16 ]
                    encryptor.encrypt(block)
    
                block = chunk[ i : i + 16 ]
                if len(block) % 16:
                    block += b'\0' * (16 - (len(block) % 16))
    
                mac_bytes = mac_encryptor.encrypt(encryptor.encrypt(block))
                await self.display(stime, tsize, len(chunk), message, progress)

            file_mac = str_to_a32(mac_bytes)
            if (file_mac[0] ^ file_mac[1], file_mac[2] ^ file_mac[3]) != meta_mac:
                raise ValueError('Mismatched mac')
        
            output_name = tlocation.name
            tlocation.close()
            shutil.move(output_name, output_path)
            return output_path

#===================================================================================================================================
    
    async def getinfo(self, url):
        fileuid, filekey = await self.parse_uri(url).split('!')
        return await self.exeinfo(fileuid, filekey)

#===================================================================================================================================

    async def exeinfo(self, file_uid, file_key):
        data = await self.api_request({'a': 'g', 'p': file_uid, 'ssm': 1})
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
