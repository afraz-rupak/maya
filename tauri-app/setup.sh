#!/bin/bash

echo "🚀 MAYA Tauri Setup Script"
echo "=========================="
echo ""

# Check if Rust is installed
if ! command -v rustc &> /dev/null; then
    echo "❌ Rust is not installed!"
    echo "Install it with: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
fi
echo "✓ Rust found: $(rustc --version)"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    echo "Install it with: brew install node"
    exit 1
fi
echo "✓ Node.js found: $(node --version)"

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed!"
    exit 1
fi
echo "✓ Python3 found: $(python3 --version)"

echo ""
echo "📦 Installing Node.js dependencies..."
npm install

echo ""
echo "📦 Fetching Rust dependencies..."
cd src-tauri
cargo fetch
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run in development mode:"
echo "  npm run dev"
echo ""
echo "To build for production:"
echo "  npm run build"
