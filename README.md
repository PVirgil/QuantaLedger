# 🔬 QuantaLedger

**QuantaLedger** is a novel blockchain system designed to preserve, verify, and timestamp scientific claims and research assertions. Unlike traditional financial or NFT blockchains, QuantaLedger is built for **truth integrity** — capturing peer-reviewed knowledge with verifiable metadata and immutability.

Deployed via **Flask on Vercel**, it offers a public-facing explorer and RESTful API to submit, mine, and review claims in a decentralized, tamper-proof format.

---

## 🚀 Features

- 📌 **Claim Submission**: Add research statements, evidence links, citations, and reviewer identity
- 🔐 **Proof-of-Work Mining**: Validate claims with customizable difficulty
- 🔗 **Hash-Linked Chain**: Immutable sequence of reviewed and verified claims
- 🌐 **Public Explorer**: HTML interface showing full block data
- 📁 **JSON Storage**: Persistent local file (`quanta_chain.json`) acts as the permanent ledger

---

## 📂 File Structure

```
/
├── quantaledger_app.py       # Main Flask application for Vercel
├── quanta_chain.json         # Persisted blockchain data
├── requirements.txt          # Dependencies (Flask)
└── vercel.json               # Vercel deployment config
```

---

## 📦 Installation (Local Testing)

```bash
pip install -r requirements.txt
python quantaledger_app.py
```

Then visit `http://localhost:5000` to explore.

---

## 🔄 API Reference

| Method | Endpoint      | Description                          |
|--------|---------------|--------------------------------------|
| GET    | `/`           | HTML explorer for the full chain     |
| GET    | `/chain`      | JSON dump of all blocks              |
| GET    | `/mine`       | Mine next submitted claim            |
| POST   | `/submit`     | Submit a new claim to be mined       |

### Example: `POST /submit`
```json
{
  "statement": "Dark matter makes up 27% of the universe.",
  "evidence": "https://example.com/research.pdf",
  "citations": ["Nature 2022", "Astrophysical Journal 2021"],
  "reviewer": "Dr. Ada Lovelace"
}
```

---

## 💡 Use Cases

- Academic claim tracking & transparency
- Immutable research publishing
- Scientific journal integration
- Verifiable AI-generated knowledge chains
- Public review and trust systems for scholarly claims

---

## 🧠 Future Enhancements

- User auth and identity binding
- Claim upvoting / flagging system
- Graph-based knowledge visualization
- Exportable citation indices

---

QuantaLedger turns scientific assertions into immutable, time-stamped entries — ensuring transparency, trust, and verifiability in a world of accelerated knowledge.
