import hashlib, json, time

class CertificateBlock:
    def __init__(self, index, certificate_data, prev_hash):
        self.index = index
        self.timestamp = time.time()
        self.certificate_data = certificate_data
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'certificate_data': self.certificate_data,
            'prev_hash': self.prev_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class CertificateBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return CertificateBlock(0, "Genesis Block", "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_certificate(self, certificate_data):
        last_block = self.get_last_block()
        new_block = CertificateBlock(len(self.chain), certificate_data, last_block.hash)
        self.chain.append(new_block)
        return new_block.hash

    def verify_certificate(self, certificate_data):
        cert_hash = hashlib.sha256(json.dumps(certificate_data, sort_keys=True).encode()).hexdigest()
        for block in self.chain:
            stored_hash = hashlib.sha256(json.dumps(block.certificate_data, sort_keys=True).encode()).hexdigest()
            if stored_hash == cert_hash:
                return True
        return False
