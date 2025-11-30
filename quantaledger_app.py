# quantaledger_app.py – QuantaLedger: Scientific Truth Blockchain for Vercel Deployment

from flask import Flask, jsonify, request, render_template_string
import hashlib
import json
import time
import os
from uuid import uuid4

CHAIN_FILE = 'quanta_chain.json'
app = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, claim_id, statement, evidence, citations, reviewer, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.claim_id = claim_id
        self.statement = statement
        self.evidence = evidence
        self.citations = citations
        self.reviewer = reviewer
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        return hashlib.sha256(json.dumps(self.__dict__, sort_keys=True).encode()).hexdigest()

class QuantaLedger:
    difficulty = 4

    def __init__(self):
        self.pending_claims = []
        self.chain = self.load_chain()

    def create_genesis_block(self):
        return [Block(0, time.time(), "GENESIS", "Genesis block", "", [], "System", "0")]

    def last_block(self):
        return self.chain[-1]

    def submit_claim(self, statement, evidence, citations, reviewer):
        claim_id = str(uuid4())
        self.pending_claims.append({
            'claim_id': claim_id,
            'statement': statement,
            'evidence': evidence,
            'citations': citations,
            'reviewer': reviewer
        })
        return claim_id

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * QuantaLedger.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        if self.last_block().hash != block.previous_hash:
            return False
        if not proof.startswith('0' * QuantaLedger.difficulty):
            return False
        if proof != block.compute_hash():
            return False
        self.chain.append(block)
        self.save_chain()
        return True

    def mine_claim(self):
        if not self.pending_claims:
            return False
        data = self.pending_claims.pop(0)
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            claim_id=data['claim_id'],
            statement=data['statement'],
            evidence=data['evidence'],
            citations=data['citations'],
            reviewer=data['reviewer'],
            previous_hash=self.last_block().hash
        )
        proof = self.proof_of_work(block)
        if self.add_block(block, proof):
            return block.index
        return False

    def save_chain(self):
        with open(CHAIN_FILE, 'w') as f:
            json.dump([block.__dict__ for block in self.chain], f, indent=4)

    def load_chain(self):
        if not os.path.exists(CHAIN_FILE):
            return self.create_genesis_block()
        with open(CHAIN_FILE, 'r') as f:
            return [Block(**b) for b in json.load(f)]

ledger = QuantaLedger()

@app.route('/')
def home():
    html = """
    <html><head><title>QuantaLedger</title><style>
    body { font-family: sans-serif; padding: 20px; background: #eef2f3; }
    .block { background: white; margin: 10px 0; padding: 15px; border-radius: 8px; box-shadow: 0 0 5px rgba(0,0,0,0.1); }
    </style></head><body>
    <h1>🔬 QuantaLedger Explorer</h1>
    {% for block in chain %}
    <div class="block">
        <h2>Block #{{ block.index }} – {{ block.statement }}</h2>
        <p><b>Claim ID:</b> {{ block.claim_id }}</p>
        <p><b>Reviewer:</b> {{ block.reviewer }}</p>
        <p><b>Evidence:</b> {{ block.evidence }}</p>
        <p><b>Citations:</b> {{ block.citations }}</p>
        <p><b>Timestamp:</b> {{ block.timestamp }}</p>
        <p><b>Hash:</b> {{ block.hash }}</p>
        <p><b>Previous Hash:</b> {{ block.previous_hash }}</p>
    </div>
    {% endfor %}
    </body></html>
    """
    return render_template_string(html, chain=ledger.chain)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    required = ('statement', 'evidence', 'citations', 'reviewer')
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing fields'}), 400
    claim_id = ledger.submit_claim(data['statement'], data['evidence'], data['citations'], data['reviewer'])
    return jsonify({'message': 'Claim submitted', 'claim_id': claim_id})

@app.route('/mine')
def mine():
    result = ledger.mine_claim()
    return jsonify({'message': f'Block #{result} mined' if result is not False else 'No claims to mine'})

@app.route('/chain')
def chain():
    return jsonify([b.__dict__ for b in ledger.chain])

app = app  # For Vercel
