"""
PIN Setup Utility for MAYA
Set or change backup PIN for face authentication
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from frontend.components.secure_storage import SecureStorage


def setup_pin():
    """Interactive PIN setup"""
    print("\n" + "="*50)
    print("  MAYA - Backup PIN Setup")
    print("="*50 + "\n")
    
    storage = SecureStorage()
    
    # Check if PIN already exists
    if not storage.secure_storage.check_first_time_setup():
        print("⚠️  A PIN already exists.")
        change = input("Do you want to change it? (yes/no): ").strip().lower()
        if change not in ['yes', 'y']:
            print("Cancelled.")
            return
    
    while True:
        pin = input("\nEnter 4-digit PIN: ").strip()
        
        if len(pin) != 4:
            print("❌ PIN must be exactly 4 digits")
            continue
        
        if not pin.isdigit():
            print("❌ PIN must contain only numbers")
            continue
        
        # Confirm PIN
        pin_confirm = input("Confirm PIN: ").strip()
        
        if pin != pin_confirm:
            print("❌ PINs don't match. Try again.")
            continue
        
        # Save PIN
        if storage.save_pin(pin):
            print("\n✅ PIN saved successfully!")
            print("   You can now use this PIN as a backup for face authentication.")
            break
        else:
            print("\n❌ Error saving PIN. Please try again.")
            return
    
    print("\n" + "="*50 + "\n")


def remove_pin():
    """Remove existing PIN"""
    print("\n" + "="*50)
    print("  MAYA - Remove PIN")
    print("="*50 + "\n")
    
    storage = SecureStorage()
    
    confirm = input("Are you sure you want to remove your PIN? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("Cancelled.")
        return
    
    # Delete PIN file
    pin_file = storage.storage_path / "pin.json"
    if pin_file.exists():
        pin_file.unlink()
        print("✅ PIN removed successfully!")
    else:
        print("⚠️  No PIN found.")
    
    print("\n" + "="*50 + "\n")


def main():
    """Main menu"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "remove":
            remove_pin()
            return
    
    setup_pin()


if __name__ == "__main__":
    main()
