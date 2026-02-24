```text
╔════════════════════════════════════════╗
║           NETSPEED CLI v1.0            ║
╚════════════════════════════════════════╝
```

A blazing fast internet speed test CLI tool with a beautiful terminal UI.

<p align="center">
  <img src="https://img.shields.io/npm/v/netspeed-cli" alt="npm version">
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
npm install -g netspeed-cli
```

### Python (pip)
```bash
pip install netspeed
```

## 🚀 Usage

```bash
netspeed
```

## 📸 Example Output

```
```ansi
  [1;36m╔════════════════════════════════════════╗[0m
  [1;36m║[0m[1;37m           NETSPEED CLI v1.0            [0m[1;36m║[0m
  [1;36m╚════════════════════════════════════════╝[0m

  [90mStarting speed test...[0m

  [1;37m┌─ PING ───────────────────────────────┐[0m
  [1;37m│[0m [33m⚡ 45 ms[0m                            [1;37m│[0m
  [1;37m└──────────────────────────────────────┘[0m

  [1;37m┌─ DOWNLOAD ───────────────────────────┐[0m
  [1;37m│[0m [32m📥 87.32 Mbps[0m                       [1;37m│[0m
  [1;37m└──────────────────────────────────────┘[0m

  [1;37m┌─ UPLOAD ─────────────────────────────┐[0m
  [1;37m│[0m [35m📤 26.20 Mbps[0m                       [1;37m│[0m
  [1;37m└──────────────────────────────────────┘[0m

  [90m────────────────────────────────────────[0m


## 🔧 Development

### Node.js
```bash
git clone https://github.com/PreeyanandaSoram/netspeed-cli.git
cd netspeed-cli/js
npm install
node bin/cli.js
```

### Python
```bash
git clone https://github.com/PreeyanandaSoram/netspeed-cli.git
cd netspeed-cli/py
pip install -r requirements.txt
python -m netspeed
```

## 📄 License

MIT License - see the [LICENSE](https://github.com/PreeyanandaSoram/netspeed-cli/blob/main/LICENSE) file.

---

<p align="center">Made with ❤️ by Preeyananda Soram</p>
