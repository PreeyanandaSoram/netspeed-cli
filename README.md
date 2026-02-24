<div align="center">

```text
╔════════════════════════════════════════╗
║           NETSPEED CLI v1.0            ║
╚════════════════════════════════════════╝
```

</div>

A blazing fast internet speed test CLI tool with a beautiful terminal UI.

<p align="center">
  <img src="https://img.shields.io/npm/v/netspeed-test-cli" alt="npm version">
  <img src="https://img.shields.io/pypi/v/netspeed" alt="PyPI version">
  <img src="https://img.shields.io/github/license/PreeyanandaSoram/netspeed-cli" alt="license">
</p>

## ✨ Features

- 🚀 Blazing fast speed test
- 🎨 Beautiful terminal UI with spinners
- 📊 Download & Upload speed measurement
- ⚡ Low-latency ping test
- 🖥️ Cross-platform (Node.js & Python)

## 📦 Installation

### Node.js (npm)
```bash
npm install -g netspeed-test-cli
```

### Python (pip)
```bash
pip install netspeed
```

## 🚀 Usage

```bash
netspeed
```

## 📸 Menu

```
┌──────────────────────────┐
│      SELECT OPTION      │
├──────────────────────────┤
│ 1.  Run Speed Test      │
│ 2.  View Version        │
│ 3.  Update              │
│ 4.  Exit                │
└──────────────────────────┘
```

## 📸 Example Output

```
┌──────────────────┐
│ NETSPEED CLI v1 │
└──────────────────┘

  Starting speed test...

  ┌─ PING ─────────────┐
  │ ⚡ 45 ms            │
  └────────────────────┘

  ┌─ DOWNLOAD ─────────┐
  │ 📥 87.32 Mbps      │
  └────────────────────┘

  ┌─ UPLOAD ───────────┐
  │ 📤 26.20 Mbps      │
  └────────────────────┘

  ____________________________________
```

## 🔧 Development

### Node.js
```bash
git clone https://github.com/Preeyananda/netspeed-cli.git
cd netspeed-cli/js
npm install
node bin/cli.js
```

### Python
```bash
git clone https://github.com/Preeyananda/netspeed-cli.git
cd netspeed-cli/py
pip install -r requirements.txt
python -m netspeed
```

## 📄 License

MIT License - see the [LICENSE](https://github.com/PreeyanandaSoram/netspeed-cli/blob/main/LICENSE) file.

---

<p align="center">Made with ❤️ by Preeyananda Soram</p>
