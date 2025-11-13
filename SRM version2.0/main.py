import sys
import datetime
import sqlite3
import csv
import subprocess
import shutil
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QStatusBar, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QGridLayout,
    QTabWidget, QComboBox, QDateEdit, QCompleter, QGroupBox, QAbstractItemView,
    QTextEdit, QSizePolicy, QSpinBox, QFileDialog, QScrollArea, QFrame,
    QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QDate, QStringListModel, QMarginsF
from PyQt6.QtGui import QColor, QFont, QDoubleValidator, QIntValidator
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QTextDocument, QPageLayout, QPageSize

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ******************************************************************************
# SECURITY NOTE: This application uses a placeholder 'default' password hash.
# In a production environment, you MUST use a secure hashing library like
# 'bcrypt' or Python's built-in 'hashlib' (e.g., PBKDF2 with SHA256).
# ******************************************************************************

# ==============================================================================
# 0. QSS THEME STYLING (UNCHANGED)
# ==============================================================================

# ==============================================================================
# 0. QSS THEME STYLING (MODIFIED FOR COMPACT NAV BUTTONS)
# ==============================================================================

# ==============================================================================
# 0. QSS THEME STYLING (MODIFIED FOR COMPACT NAV BUTTONS)
# ==============================================================================

# ==============================================================================
# 0. QSS THEME STYLING (MODIFIED FOR COMPACT NAV BUTTONS AND SAFE GEOMETRY)
# ==============================================================================

# ==============================================================================
# 0. QSS THEME STYLING (MODIFIED FOR COMPACT NAV BUTTONS AND SAFE GEOMETRY)
# ==============================================================================

QSS_THEME = """
/**************************************************
 * GLOBAL COLORS & FONTS - MONOCHROMATIC PROFESSIONAL MEDICAL TEAL THEME
 **************************************************/
/* Main Palette: Professional Teal/Cyan, Gray, and White */
QWidget {
    font-family: "Segoe UI", "Tahoma", sans-serif;
    font-size: 10pt;
    background-color: #F8F9FA; /* Light Gray background */
    color: #343A40; /* Dark Gray text */
}

/* Primary Medical Teal (Main Action, POS) */
.TealPrimary { background-color: #008080; color: white; } /* Deep Teal */
/* Secondary Action/Navigation Gray */
.GraySecondary { background-color: #6C757D; color: white; }
/* Accent/Reports/Warning Gray */
.GrayAccent { background-color: #495057; color: white; }
/* Danger/Critical/Expired Red */
.RedCritical { background-color: #C82333; color: white; } /* Deeper, more serious red */

/* --- INPUTS & WIDGETS (Uniform Sizing for POS) --- */

/* Uniform padding and style for all input fields */
QLineEdit, QComboBox, QDateEdit, QSpinBox, QTextEdit {
    border: 1px solid #CED4DA; 
    padding: 8px 10px;
    border-radius: 4px;
    background-color: white;
    min-height: 28px; /* Standardized minimum height */
    font-size: 10pt; /* Standardized font size */
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QTextEdit:focus {
    border: 1px solid #008080; /* Focus Teal */
}
QLabel {
    font-size: 10pt; /* Ensure label text matches input text size */
}

QPushButton {
    border: none;
    padding: 10px;
    border-radius: 4px;
    min-height: 28px; /* Standardized minimum height */
    font-weight: 500; 
}
QPushButton:hover {
    opacity: 0.9;
}

/* Apply professional colors to buttons by property class */
/* GreenButton class is now TealPrimary */
QPushButton[class="GreenButton"] { background-color: #008080; color: white; } 
/* BlueButton class is now GraySecondary */
QPushButton[class="BlueButton"] { background-color: #6C757D; color: white; } 
/* OrangeButton class is now GrayAccent */
QPushButton[class="OrangeButton"] { background-color: #495057; color: white; } 
/* RedButton class remains RedCritical */
QPushButton[class="RedButton"] { background-color: #C82333; color: white; } 
/* ReturnButton class remains GrayAccent */
QPushButton[class="ReturnButton"] { background-color: #495057; color: white; } 

#NavButton {
    min-width: 100px; /* REDUCED to 100px for more compactness */
    text-align: left;
    padding-left: 5px; /* Reduced padding-left to 5px */
    font-weight: bold;
    font-size: 9pt; /* Reduced font size for compactness */
    border-left: 4px solid transparent; 
}
#NavButton:checked, #NavButton:hover {
    border-left: 4px solid #008080; /* Teal indicator on hover/active */
}


/**************************************************
 * DASHBOARD & CONTAINERS
 **************************************************/
QGroupBox {
    font-weight: bold;
    font-size: 11pt;
    margin-top: 10px;
    padding-top: 15px;
}

/* Dashboard Card Styles */
.Card {
    background-color: white;
    border: 1px solid #DEE2E6; 
    border-radius: 6px;
    padding: 15px;
    margin: 5px;
}
.CardTitle {
    font-size: 10pt;
    font-weight: 500;
    margin-bottom: 5px;
    color: #6C757D; 
}
.CardValue {
    font-size: 18pt;
    font-weight: bold;
    color: #343A40; 
}

/**************************************************
 * TABLES (QTableWidget)
 **************************************************/
QTableWidget {
    border: 1px solid #DEE2E6;
    gridline-color: #E9ECEF;
    border-radius: 4px;
    background-color: white;
}
QHeaderView::section {
    background-color: #E9ECEF;
    color: #343A40;
    padding: 10px 8px;
    border: 0;
    border-right: 1px solid #DEE2E6;
    font-weight: bold;
}
QTableWidget::item:selected {
    background-color: #E6F5F5; /* Light Teal selection */
    color: #343A40;
}

/**************************************************
 * TAB WIDGETS
 **************************************************/
QTabWidget::pane {
    border: 1px solid #CED4DA;
    border-radius: 4px;
    background-color: white;
}
QTabBar::tab {
    background: #E9ECEF;
    border: 1px solid #CED4DA;
    border-bottom-color: #E9ECEF;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 8px 15px;
    color: #343A40;
}
QTabBar::tab:selected {
    background: white;
    border-color: #CED4DA;
    border-bottom-color: white;
    font-weight: bold;
}
"""



# ==============================================================================
# 1. DATABASE MANAGER (THE DATA ENGINE) - COMPLETE REPLACEMENT
# ==============================================================================

# ==============================================================================
# 1. DATABASE MANAGER (THE DATA ENGINE) - COMPLETE REPLACEMENT
# ==============================================================================

# ==============================================================================
# 1. DATABASE MANAGER (THE DATA ENGINE) - COMPLETE REPLACEMENT
# ==============================================================================

# ==============================================================================
# 1. DATABASE MANAGER (THE DATA ENGINE) - COMPLETE REPLACEMENT (FINAL WITH PRODUCT HISTORY)
# ==============================================================================

class DatabaseManager:
    """Handles all SQLite database connections and operations, including configuration settings."""

    def __init__(self, db_name="pharmacy_pos.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        try:
            # Use isolation_level=None for autocommit mode
            self.conn = sqlite3.connect(self.db_name, isolation_level=None)
            self.cursor = self.conn.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON")
        except sqlite3.Error as e:
            print(f"❌ Database connection error: {e}")
            self.conn = None
            self.cursor = None

    def create_tables(self):
        if not self.conn: return

        # 1. Classes, 2. Suppliers, 2.5. Companies, 2.7. Doctors (Unchanged Structure)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS classes (class_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS suppliers (supplier_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS companies (company_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS doctors (doctor_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL)")

        # >>> Supplier Contact/Master Table <<<
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS supplier_contact (
                supplier_contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_name TEXT UNIQUE NOT NULL,
                contact_person TEXT,
                phone TEXT,
                email TEXT,
                address TEXT
            )
        """)
        # 3. Products Master Table (PRICES REMOVED - Static info only)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                class_id INTEGER,
                units_per_pack INTEGER NOT NULL DEFAULT 1,  
                unit_type TEXT NOT NULL DEFAULT 'PIECE',  
                company TEXT,
                supplier TEXT,  
                formulation TEXT,
                reorder_point INTEGER DEFAULT 50,  
                FOREIGN KEY (class_id) REFERENCES classes (class_id)
            )
        """)

        # 4. PURCHASE ORDERS, 5. PURCHASE ITEMS, 6. SUPPLIER PAYMENTS (Unchanged Structure)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchase_orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT, supplier_name TEXT NOT NULL, order_date TEXT NOT NULL,
                invoice_number TEXT, invoice_date TEXT, total_invoice_amount REAL DEFAULT 0.0,
                status TEXT NOT NULL, pending_amount_override REAL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchase_items (
                p_item_id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER NOT NULL, product_id INTEGER NOT NULL,
                batch_number TEXT, pack_quantity_ordered REAL NOT NULL, pack_cost_price REAL NOT NULL, date_received TEXT,  
                FOREIGN KEY (order_id) REFERENCES purchase_orders (order_id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products (product_id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS supplier_payments (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER, payment_date TEXT NOT NULL,
                amount_paid REAL NOT NULL, payment_method TEXT, transaction_ref TEXT, notes TEXT, user_id INTEGER,
                FOREIGN KEY (order_id) REFERENCES purchase_orders (order_id) ON DELETE SET NULL, FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # 7. Stock Batches Table (PRICES ADDED TO BATCH LEVEL)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_batches (
                batch_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                purchase_item_id INTEGER,  
                batch_number TEXT,  
                stock_quantity REAL NOT NULL,  
                expiry_date TEXT NOT NULL,  
                date_received TEXT NOT NULL,  
                pack_cost_price REAL NOT NULL,      
                pack_selling_price REAL NOT NULL,    
                FOREIGN KEY (product_id) REFERENCES products (product_id),
                FOREIGN KEY (purchase_item_id) REFERENCES purchase_items (p_item_id) ON DELETE SET NULL
            )
        """)
        
        # 8-12. Users, Sales, Sale_Items, Returns, Audit_Log (Unchanged Structure)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, role TEXT NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_date TEXT NOT NULL, total_amount REAL NOT NULL, discount REAL DEFAULT 0.0, payment_method TEXT, user_id INTEGER, doctor_ref TEXT, patient_name TEXT, patient_address TEXT, status TEXT NOT NULL DEFAULT 'Finalized', FOREIGN KEY (user_id) REFERENCES users (id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sale_items (id INTEGER PRIMARY KEY AUTOINCREMENT, sale_id INTEGER NOT NULL, product_id INTEGER NOT NULL, batch_id INTEGER, quantity_sold REAL NOT NULL, unit_price REAL NOT NULL, cost_price_at_sale REAL NOT NULL, FOREIGN KEY (sale_id) REFERENCES sales (id), FOREIGN KEY (product_id) REFERENCES products (product_id), FOREIGN KEY (batch_id) REFERENCES stock_batches (batch_id) ON DELETE SET NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS returns (return_id INTEGER PRIMARY KEY AUTOINCREMENT, return_date TEXT NOT NULL, product_id INTEGER NOT NULL, batch_id INTEGER NOT NULL, order_id INTEGER, quantity_returned_packs REAL NOT NULL, cost_price_at_return REAL NOT NULL, total_refund_value REAL NOT NULL, supplier_name TEXT, reason TEXT NOT NULL, FOREIGN KEY (product_id) REFERENCES products (product_id), FOREIGN KEY (batch_id) REFERENCES stock_batches (batch_id) ON DELETE RESTRICT, FOREIGN KEY (order_id) REFERENCES purchase_orders (order_id) ON DELETE SET NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS audit_log (log_id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, user_id INTEGER, username TEXT NOT NULL, action TEXT NOT NULL, context_id INTEGER, details TEXT, FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL)")

        # >>> Settings Table <<<
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY NOT NULL,
                value TEXT
            )
        """)
        
        # Schema Migration/Check (for status column)
        try:
            self.cursor.execute("SELECT status FROM sales LIMIT 1")
        except sqlite3.OperationalError:
            self.cursor.execute("ALTER TABLE sales ADD COLUMN status TEXT DEFAULT 'Finalized'")
            
        try:
            self.cursor.execute("SELECT status FROM purchase_orders LIMIT 1")
        except sqlite3.OperationalError:
            self.cursor.execute("ALTER TABLE purchase_orders ADD COLUMN status TEXT DEFAULT 'Received/Unpaid'")

        self.conn.commit()
    
    # --- AUDIT LOG METHOD (Unchanged) ---
    def log_action(self, user_id, username, action, context_id=None, details=""):
        """Records an action into the audit log."""
        if not self.conn: return
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            with self.conn:
                self.cursor.execute(
                    """INSERT INTO audit_log (timestamp, user_id, username, action, context_id, details)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                    (timestamp, user_id, username, action, context_id, details)
                )
        except sqlite3.Error as e:
            print(f"❌ Error logging action: {e}")

    # --- PURCHASING & PAYABLES METHODS (Unchanged) ---
    
    def create_purchase_order(self, supplier_name, items):
        """Creates a new PO and related items (Status: 'Received/Unpaid')."""
        current_date = datetime.date.today().strftime('%Y-%m-%d')
        total_amount = sum(item['pack_quantity'] * item['pack_cost'] for item in items)
        
        try:
            with self.conn:
                # 1. Create Purchase Order Header
                self.cursor.execute(
                    """INSERT INTO purchase_orders (supplier_name, order_date, total_invoice_amount, status)
                        VALUES (?, ?, ?, ?)""",
                    (supplier_name, current_date, total_amount, 'Received/Unpaid')
                )
                order_id = self.cursor.lastrowid
                
                # 2. Insert Purchase Items and Stock Batches
                for item in items:
                    # 2a. Insert into purchase_items
                    self.cursor.execute(
                        """INSERT INTO purchase_items (order_id, product_id, batch_number, pack_quantity_ordered, pack_cost_price, date_received)
                            VALUES (?, ?, ?, ?, ?, ?)""",
                        (order_id, item['product_id'], item['batch_number'], item['pack_quantity'], item['pack_cost'], current_date)
                    )
                    p_item_id = self.cursor.lastrowid
                    
                    # 2b. Insert into stock_batches (INCLUDING BATCH PRICES)
                    self.cursor.execute(
                        """INSERT INTO stock_batches (product_id, purchase_item_id, batch_number, stock_quantity, expiry_date, date_received, pack_cost_price, pack_selling_price)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (item['product_id'], p_item_id, item['batch_number'], item['pack_quantity'], item['expiry_date'], current_date, item['pack_cost'], item['pack_selling_price'])
                    )
            
            return order_id
        except sqlite3.Error as e:
            print(f"Error creating purchase order: {e}")
            return None

    def record_supplier_payment(self, order_id, amount_paid, payment_method, transaction_ref, notes, user_id):
        """Records a payment against a specific purchase order/invoice."""
        if amount_paid <= 0: return False
        
        current_date = datetime.date.today().strftime('%Y-%m-%d')
        
        try:
            with self.conn:
                # MODIFIED INSERT: Added transaction_ref and notes
                self.cursor.execute(
                    """INSERT INTO supplier_payments (order_id, payment_date, amount_paid, payment_method, transaction_ref, notes, user_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (order_id, current_date, amount_paid, payment_method, transaction_ref, notes, user_id)
                )
                
                # Simple status update: if net pending is zero, mark as paid.
                pending_amount = self.get_order_pending_amount(order_id)
                if pending_amount <= 0.001:
                    self.cursor.execute("UPDATE purchase_orders SET status = 'Paid' WHERE order_id = ?", (order_id,))
                
            return True
        except sqlite3.Error as e:
            print(f"Error recording supplier payment: {e}")
            return False

    def get_supplier_pending_invoices(self):
        """Retrieves invoices that are not fully paid or have open balances."""
        query = """
        SELECT 
            T1.order_id,
            T1.supplier_name,
            T1.invoice_number,
            T1.total_invoice_amount,
            COALESCE(SUM(T2.amount_paid), 0.0) AS total_paid,
            T1.status
        FROM purchase_orders AS T1
        LEFT JOIN supplier_payments AS T2 ON T1.order_id = T2.order_id
        WHERE T1.status != 'Voided'
        GROUP BY T1.order_id
        HAVING T1.total_invoice_amount > total_paid 
        ORDER BY T1.order_date DESC;
        """
        self.cursor.execute(query)
        
        # Integrate returns credit calculation before final presentation
        results = []
        for order_id, supplier_name, invoice_number, total_invoice_amount, total_paid, status in self.cursor.fetchall():
            return_credit = self.get_order_returns_credit(order_id)
            net_paid = total_paid + return_credit # Credit acts like a payment
            pending = total_invoice_amount - net_paid
            
            # Re-check pending status > 0 for this function
            if pending > 0.001:
                results.append({
                    'order_id': order_id,
                    'supplier_name': supplier_name,
                    'invoice_number': invoice_number or 'N/A',
                    'total_invoice_amount': total_invoice_amount,
                    'total_paid': total_paid,
                    'return_credit': return_credit,
                    'net_pending': pending,
                    'status': status
                })
        return results

    def get_order_pending_amount(self, order_id):
        """Calculates the net pending amount for a single order."""
        query = "SELECT total_invoice_amount FROM purchase_orders WHERE order_id = ?"
        self.cursor.execute(query, (order_id,))
        total_invoice_amount = self.cursor.fetchone()
        if not total_invoice_amount: return 0.0
        total_invoice_amount = total_invoice_amount[0]
        
        # Sum payments
        self.cursor.execute("SELECT COALESCE(SUM(amount_paid), 0.0) FROM supplier_payments WHERE order_id = ?", (order_id,))
        total_paid = self.cursor.fetchone()[0]

        # Sum returns credit
        return_credit = self.get_order_returns_credit(order_id)
        
        return max(0.0, total_invoice_amount - (total_paid + return_credit))

    def get_order_returns_credit(self, order_id):
        """Calculates the total return credit applied to a specific order."""
        query = "SELECT COALESCE(SUM(total_refund_value), 0.0) FROM returns WHERE order_id = ?"
        self.cursor.execute(query, (order_id,))
        return self.cursor.fetchone()[0] or 0.0
    
    def get_purchase_order_details(self, order_id):
        """Retrieves all header, line items, and payment details for a specific PO."""
        if not self.conn: return None
        
        # 1. Fetch Header Details (UNCHANGED)
        self.cursor.execute("SELECT order_id, supplier_name, order_date, total_invoice_amount, status, invoice_number, invoice_date FROM purchase_orders WHERE order_id = ?", (order_id,))
        header_data = self.cursor.fetchone()
        if not header_data: return None

        # 2. Fetch Line Items (UNCHANGED)
        query_items = """
        SELECT T1.p_item_id, T2.name, T1.batch_number, T1.pack_quantity_ordered, T1.pack_cost_price, T2.units_per_pack, T2.unit_type
        FROM purchase_items AS T1
        JOIN products AS T2 ON T1.product_id = T2.product_id
        WHERE T1.order_id = ?
        """
        self.cursor.execute(query_items, (order_id,))
        line_items = self.cursor.fetchall()

        # 3. Fetch Payment/Return Summary (UNCHANGED)
        self.cursor.execute("SELECT COALESCE(SUM(amount_paid), 0.0) FROM supplier_payments WHERE order_id = ?", (order_id,))
        total_payments = self.cursor.fetchone()[0] or 0.0
        total_credit = self.get_order_returns_credit(order_id)
        
        return {
            'header': {
                'id': header_data[0], 'supplier': header_data[1], 'order_date': header_data[2],
                'total_invoice': header_data[3], 'status': header_data[4],
                'invoice_number': header_data[5], 'invoice_date': header_data[6]
            },
            'items': line_items,
            'summary': {'paid': total_payments, 'credit': total_credit, 'pending': header_data[3] - total_payments - total_credit}
        }

    def soft_void_purchase_order(self, order_id, user_id):
        """
        Voids a purchase order, reverts stock, clears payables, and updates PO status.
        Only works if no PAYMENTS or RETURNS have been made against the PO.
        """
        if not self.conn: return "DB connection inactive."
        
        # 1. Check if the order has been paid or credited (Full Payment/Credit Forbids Void)
        summary = self.get_purchase_order_details(order_id)
        if not summary:
            return f"PO {order_id} not found."
            
        if summary['summary']['paid'] > 0.001:
            return "Order has recorded payments and cannot be fully voided. Use Supplier Returns to process stock disposal."
        if summary['summary']['credit'] > 0.001:
            return "Order has recorded returns (credit notes) and cannot be fully voided."

        try:
            with self.conn:
                # 2. Fetch Items and Batches to Revert
                self.cursor.execute("SELECT p_item_id, product_id, pack_quantity_ordered FROM purchase_items WHERE order_id = ?", (order_id,))
                items = self.cursor.fetchall()
                
                reverted_items = 0
                
                for p_item_id, product_id, packs_ordered in items:
                    # 2a. Find the corresponding batch and revert stock
                    self.cursor.execute("SELECT batch_id, stock_quantity FROM stock_batches WHERE purchase_item_id = ?", (p_item_id,))
                    batch_data = self.cursor.fetchone()
                    
                    if batch_data:
                        batch_id, current_stock = batch_data
                        
                        # Deduct the ordered quantity from stock (must account for partial sales)
                        qty_to_revert = packs_ordered
                        if current_stock < packs_ordered:
                            # If stock is already less than ordered (due to sales), only revert remaining stock.
                            print(f"PO Void Warning: Batch {batch_id} for PO {order_id} only had {current_stock:.2f} packs left. Reverting remaining stock.")
                            qty_to_revert = current_stock

                        self.cursor.execute("UPDATE stock_batches SET stock_quantity = ROUND(stock_quantity - ?, 3) WHERE batch_id = ?",
                                             (qty_to_revert, batch_id))
                        
                        # Remove purchase_item record
                        self.cursor.execute("DELETE FROM purchase_items WHERE p_item_id = ?", (p_item_id,))
                        
                        # Remove stock_batch record if quantity is now 0 and no sales/returns history exists.
                        self.cursor.execute("DELETE FROM stock_batches WHERE batch_id = ? AND stock_quantity <= 0.001 AND (SELECT COUNT(*) FROM sale_items WHERE batch_id = ?) = 0 AND (SELECT COUNT(*) FROM returns WHERE batch_id = ?) = 0",
                                             (batch_id, batch_id, batch_id))
                        reverted_items += 1

                # 3. Update PO Header Status & Amount
                self.cursor.execute("UPDATE purchase_orders SET status = 'Voided', total_invoice_amount = 0.0, pending_amount_override = 0.0 WHERE order_id = ?", (order_id,))

                # 4. Log the Void Action
                user_info = self.cursor.execute("SELECT username FROM users WHERE id=?", (user_id,)).fetchone()
                username = user_info[0] if user_info else 'System'
                self.log_action(
                    user_id, username, 'PO_VOIDED', order_id,
                    f"Full PO Void. Original Total: ${summary['header']['total_invoice']:.2f}. Reverted {reverted_items} batches."
                )
                
                return True

        except sqlite3.Error as e:
            return f"Database Error during PO void: {e}"
        except Exception as e:
            return f"Critical Error during PO void: {e}"

    # --- SALES & RETURN OVERRIDES (All methods unchanged as they use base_unit prices) ---
    
    def record_return_and_deduct_stock(self, product_id, batch_id, quantity_returned_packs, cost_price, total_refund_value, supplier_name, reason):
        """
        Inserts return record (Supplier Return), links to a purchase order if possible, and updates stock_batches.
        """
        if not self.conn: return False
        current_date = datetime.date.today().strftime('%Y-%m-%d')

        # Try to find the original purchase order ID via the batch
        order_id = None
        self.cursor.execute("""
            SELECT T2.order_id FROM stock_batches AS T1
            LEFT JOIN purchase_items AS T2 ON T1.purchase_item_id = T2.p_item_id
            WHERE T1.batch_id = ?
        """, (batch_id,))
        result = self.cursor.fetchone()
        if result:
            order_id = result[0]

        try:
            with self.conn:
                # 1. Insert into Returns table
                self.cursor.execute(
                    """INSERT INTO returns (return_date, product_id, batch_id, order_id, quantity_returned_packs, cost_price_at_return, total_refund_value, supplier_name, reason)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (current_date, product_id, batch_id, order_id, quantity_returned_packs, cost_price, total_refund_value, supplier_name, reason)
                )

                # 2. Update Stock Batches (Deduct the returned quantity)
                self.cursor.execute(
                    "UPDATE stock_batches SET stock_quantity = ROUND(stock_quantity - ?, 3) WHERE batch_id = ?",
                    (quantity_returned_packs, batch_id)
                )

            return True
        except sqlite3.IntegrityError:
            print("Integrity Error during supplier return. Check if batch_id exists and all constraints are met.")
            return False
        except Exception as e:
            print(f"Error during supplier return: {e}")
            return False

    def record_sales_return_and_restore_stock(self, sale_id, product_name, qty_returned_base_units, reason, user_id):
        """
        Records a partial customer return, adds stock back to the original batch, and calculates refund/credit.
        """
        if not self.conn: return None, "DB connection inactive."

        try:
            with self.conn:
                # 1. Find the Sale Item for the returned product in the given sale_id
                self.cursor.execute("""
                    SELECT 
                        si.id, si.product_id, si.batch_id, si.quantity_sold, si.unit_price, si.cost_price_at_sale,
                        p.units_per_pack, p.unit_type
                    FROM sale_items si
                    JOIN products p ON si.product_id = p.product_id
                    JOIN sales s ON si.sale_id = s.id
                    WHERE s.id = ? AND p.name = ?
                    ORDER BY si.id DESC
                    LIMIT 1
                """, (sale_id, product_name))

                sale_item_data = self.cursor.fetchone()

                if not sale_item_data:
                    return None, f"Product '{product_name}' not found in Invoice #{sale_id}."

                si_id, product_id, batch_id, quantity_sold_units, unit_price_at_sale, cost_price_at_sale, units_per_pack, unit_type = sale_item_data

                if qty_returned_base_units > quantity_sold_units + 0.001:
                    return None, f"Return quantity ({qty_returned_base_units:.2f} units) exceeds original quantity sold ({quantity_sold_units:.2f} units)."

                # 2. Calculate Refund Value 
                refund_value = round(qty_returned_base_units * unit_price_at_sale, 2)

                # 3. Calculate Packs to restore (for stock_batches) and Cost price at return (for returns table)
                packs_per_unit = units_per_pack if units_per_pack > 0 else 1
                packs_to_restore = round(qty_returned_base_units / packs_per_unit, 3)
                cost_price_per_pack = cost_price_at_sale * packs_per_unit # Cost price per pack for returns table

                # 4. Insert into Returns Table
                self.cursor.execute(
                    """INSERT INTO returns (return_date, product_id, batch_id, order_id, quantity_returned_packs, cost_price_at_return, total_refund_value, supplier_name, reason)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (datetime.date.today().strftime('%Y-%m-%d'), product_id, batch_id, None, packs_to_restore, cost_price_per_pack, refund_value, f'Customer Return from Invoice {sale_id}', reason)
                )
                return_id = self.cursor.lastrowid
                
                # 5. Restore Stock in the original batch
                self.cursor.execute(
                    "UPDATE stock_batches SET stock_quantity = ROUND(stock_quantity + ?, 3) WHERE batch_id = ?",
                    (packs_to_restore, batch_id)
                )
                
                # 6. Log the Action
                user_info = self.cursor.execute("SELECT username FROM users WHERE id=?", (user_id,)).fetchone()
                username = user_info[0] if user_info else 'System'
                self.log_action(
                    user_id,
                    username,
                    'SALES_PARTIAL_RETURN',
                    return_id,
                    f"Invoice {sale_id}, Product: {product_name}, Units: {qty_returned_base_units:.2f}, Refund: ${refund_value:.2f}"
                )

            return refund_value, f"Return of {qty_returned_base_units:.2f} units processed. Refund/Credit: ${refund_value:.2f}"
            
        except sqlite3.Error as e:
            print(f"❌ Error processing sales return: {e}")
            return None, f"Database Error: {e}"

    def soft_void_sale_transaction(self, sale_id, user_id):
        """
        Voids a sale transaction by reversing stock movements based on net quantity sold
        (accounting for prior customer returns), logging the reversal, and setting 
        the sale status to 'Voided'.
        """
        if not self.conn: return "DB connection inactive."

        try:
            with self.conn:
                # 1. Check current status
                self.cursor.execute("SELECT status FROM sales WHERE id = ?", (sale_id,))
                current_status = self.cursor.fetchone()
                if not current_status:
                    return f"Invoice {sale_id} not found."
                if current_status[0] == 'Voided':
                    return f"Invoice {sale_id} is already Voided."

                # 2. FETCH all items sold (needed for reversal)
                self.cursor.execute("""
                    SELECT 
                        si.product_id, si.batch_id, si.quantity_sold, si.unit_price, si.cost_price_at_sale, 
                        p.units_per_pack, p.name, b.expiry_date
                    FROM sale_items si
                    JOIN products p ON si.product_id = p.product_id
                    LEFT JOIN stock_batches b ON si.batch_id = b.batch_id
                    WHERE si.sale_id = ?
                """, (sale_id,))
                sale_items = self.cursor.fetchall()

                if not sale_items:
                    # If there are no items, just mark the header as voided.
                    self.cursor.execute("UPDATE sales SET status = 'Voided', total_amount = 0.0, discount = 0.0 WHERE id = ?", (sale_id,))
                    return True 

                # 3. Revert Stock, Insert Reversal Return, and Log
                total_reversal_amount = 0.0
                reversed_count = 0
                today = datetime.date.today().strftime('%Y-%m-%d')
                
                for item in sale_items:
                    product_id, batch_id, qty_sold_units, unit_price_at_sale, cost_price_at_sale, units_per_pack, product_name, expiry_date = item
                    
                    packs_per_unit = units_per_pack if units_per_pack > 0 else 1
                    cost_price_per_pack = cost_price_at_sale * packs_per_unit

                    # --- CRITICAL FIX: Calculate total quantity already returned by customers ---
                    
                    # 1. Calculate total PACKS previously restored via CUSTOMER returns for this batch
                    self.cursor.execute("""
                        SELECT COALESCE(SUM(quantity_returned_packs), 0.0) 
                        FROM returns 
                        WHERE batch_id = ? AND supplier_name LIKE 'Customer Return from Invoice %'
                    """, (batch_id,))
                    total_packs_previously_returned = self.cursor.fetchone()[0] or 0.0
                    
                    # 2. Convert to base units sold
                    units_previously_returned = total_packs_previously_returned * packs_per_unit

                    # 3. Determine the net base units and packs to restore
                    qty_to_restore_units = max(0.0, qty_sold_units - units_previously_returned)
                    packs_to_restore = round(qty_to_restore_units / packs_per_unit, 3)

                    # If there's nothing left to restore, skip this item
                    if packs_to_restore <= 0.001:
                        print(f"Skipping void restoration for {product_name} (Batch {batch_id}). Quantity already fully returned via customer return.")
                        continue 
                    
                    # --- End CRITICAL FIX ---

                    # Calculate the net financial impact for the audit log
                    refund_value_net = round(qty_to_restore_units * unit_price_at_sale, 2)
                    total_reversal_amount += refund_value_net

                    # a. Insert full reversal into Returns table (The Auditable reversal record)
                    self.cursor.execute(
                        """INSERT INTO returns (return_date, product_id, batch_id, order_id, quantity_returned_packs, cost_price_at_return, total_refund_value, supplier_name, reason)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (today, product_id, batch_id, None, packs_to_restore, cost_price_per_pack, refund_value_net, f'VOID SALE {sale_id}', 'Full Sale Void/Reversal (Net of Customer Returns)')
                    )
                    
                    # b. Restore Stock in the original batch
                    self.cursor.execute(
                        "UPDATE stock_batches SET stock_quantity = ROUND(stock_quantity + ?, 3) WHERE batch_id = ?",
                        (packs_to_restore, batch_id)
                    )
                    reversed_count += 1

                # 4. Update the original sale status (Soft Void)
                self.cursor.execute("UPDATE sales SET status = 'Voided', total_amount = 0.0, discount = 0.0 WHERE id = ?", (sale_id,))

                # 5. Log the reversal (Void) action
                user_info = self.cursor.execute("SELECT username FROM users WHERE id=?", (user_id,)).fetchone()
                username = user_info[0] if user_info else 'System'
                self.log_action(
                    user_id,
                    username,
                    'SALE_VOIDED_SOFT',
                    sale_id,
                    f"Soft Void of Invoice {sale_id}. Items net restored: {reversed_count}, Total Net Reversed Value: ${total_reversal_amount:.2f}. Sale record kept and marked 'Voided'."
                )

            return True

        except sqlite3.Error as e:
            print(f"Database Error during void process: {e}")
            return f"Database Error during void process: {e}"
        except Exception as e:
            print(f"Critical Error during void process: {e}")
            return f"Critical Error during void process: {e}"


    # --- NEW DAILY SALES METHOD (UNCHANGED) ---
    def get_daily_sales_and_profit(self, target_date):
        """Fetches finalized sales data including calculated gross profit for a specific day."""
        if not self.conn: return []

        # 1. Base Query for Sales Headers
        query_sales = """
        SELECT id, transaction_date, total_amount, discount, patient_name, doctor_ref
        FROM sales
        WHERE DATE(transaction_date) = ? AND status = 'Finalized'
        ORDER BY transaction_date ASC;
        """
        self.cursor.execute(query_sales, (target_date,))
        sales_headers = self.cursor.fetchall()
        
        report_results = []
        
        # 2. Iterate and calculate Gross Profit for each sale
        for sale_id, datetime_str, revenue, discount, patient_name, doctor_ref in sales_headers:
            
            # Fetch COGS for this entire sale
            query_cogs = """
            SELECT COALESCE(SUM(quantity_sold * cost_price_at_sale), 0.0) 
            FROM sale_items 
            WHERE sale_id = ?;
            """
            self.cursor.execute(query_cogs, (sale_id,))
            total_cogs = self.cursor.fetchone()[0] or 0.0
            
            gross_profit = revenue - total_cogs
            time_only = datetime_str.split(' ')[1][:5] # HH:MM
            
            report_results.append({
                'id': sale_id,
                'time': time_only,
                'patient': patient_name or 'CASH SALES',
                'doctor': doctor_ref or 'N/A',
                'revenue': revenue,
                'discount': discount,
                'profit': gross_profit,
                'cogs': total_cogs
            })
            
        return report_results

    # --- INVENTORY/SETUP UTILITIES (Modified for Dynamic Pricing) ---

    def get_supplier_names(self):
        """Retrieves all unique supplier names (combining supplier and purchase_orders)."""
        if not self.conn: return []
        
        query = """
        SELECT name FROM suppliers 
        UNION 
        SELECT supplier_name FROM purchase_orders 
        UNION
        SELECT supplier_name FROM supplier_contact
        ORDER BY name ASC
        """
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]
        
    def add_initial_data(self):
        """Creates the bare minimum data (Admin user) and inserts default classes."""
        if not self.conn: return 0

        DEFAULT_CLASSES = [
            'TABLET', 'SYRUP', 'OINTMENT', 'POWDER', 'SPRAY',
            'INJECTIBLE', 'DROP', 'VIAL', 'CAPSULE', 'MISCELLANEOUS'
        ]

        try:
            with self.conn:
                # 1. Ensure the default Admin user is created
                self.cursor.execute("SELECT id FROM users WHERE username = 'Admin'")
                admin_id = self.cursor.fetchone()
                if admin_id is None:
                    # NOTE: Password hash placeholder!
                    self.cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", ('Admin', 'default', 'Admin'))
                    admin_id = self.cursor.lastrowid
                else:
                    admin_id = admin_id[0]

                # 2. Setup product classes
                for class_name in DEFAULT_CLASSES:
                    self.cursor.execute("INSERT OR IGNORE INTO classes (name) VALUES (?)", (class_name,))
                
            return admin_id

        except sqlite3.Error as e:
            print(f"Error during initial data setup: {e}")
            return 0

    def get_expiry_alerts(self):
        """Retrieves batches that are expired, or expiring in the next 60 days. (UNCHANGED)"""
        if not self.conn: return {'expired': [], '1_month': [], '2_month': []}
        
        query = """
        SELECT  
            T1.name, T2.date_received, T2.stock_quantity, T2.expiry_date, T1.units_per_pack, T1.unit_type, T2.batch_number
        FROM products AS T1
        JOIN stock_batches AS T2 ON T1.product_id = T2.product_id
        WHERE T2.stock_quantity > 0 AND T2.expiry_date <= STRFTIME('%Y-%m', 'now', '+60 days')
        ORDER BY T2.expiry_date ASC;
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        alerts = {'expired': [], '1_month': [], '2_month': []}
        today_date = datetime.date.today()
        today_yyyymm = today_date.strftime('%Y-%m')
        
        for name, date_received, pack_qty, expiry_date_str, units_per_pack, unit_type, batch_number in results:
            
            try:
                # Use the 1st of the expiry month for date comparison logic
                expiry_month_start = datetime.datetime.strptime(expiry_date_str, '%Y-%m').date()
                days_to_expiry = (expiry_month_start - today_date).days
            except ValueError:  
                continue
            
            if unit_type == 'TABLET':
                base_unit_qty = int(pack_qty * units_per_pack)
                pack_unit = 'Strips'
                base_unit = 'tabs'
            else:
                base_unit_qty = int(pack_qty)  
                pack_unit = unit_type.capitalize() + 's' if unit_type not in ['MISCELLANEOUS', 'SYRUP', 'OINTMENT'] else unit_type.capitalize()
                base_unit = pack_unit.lower()
            
            item = f"{name} (Batch: {batch_number}, Received: {date_received}) - Stock: {pack_qty:.2f} {pack_unit} ({base_unit_qty} {base_unit}), Expires: {expiry_date_str}"
            
            if expiry_date_str < today_yyyymm:
                alerts['expired'].append(item)
            elif days_to_expiry <= 30:
                alerts['1_month'].append(item)
            elif days_to_expiry <= 60:
                alerts['2_month'].append(item)
                
        return alerts

    def get_expired_batches(self):
        """Retrieves ONLY batches that have an expiry date less than today (YYYY-MM). (UNCHANGED)"""
        if not self.conn: return []
        today_yyyymm = datetime.date.today().strftime('%Y-%m')
        
        query = """
        SELECT  
            T1.name, T2.date_received, T2.stock_quantity, T2.expiry_date, T1.units_per_pack, T1.unit_type, T2.batch_number
        FROM products AS T1
        JOIN stock_batches AS T2 ON T1.product_id = T2.product_id
        WHERE T2.stock_quantity > 0 AND T2.expiry_date < ?
        ORDER BY T2.expiry_date ASC;
        """
        self.cursor.execute(query, (today_yyyymm,))
        results = self.cursor.fetchall()
        
        expired_list = []
        for name, date_received, pack_qty, expiry_date_str, units_per_pack, unit_type, batch_number in results:
            
            if unit_type == 'TABLET':
                base_unit_qty = int(pack_qty * units_per_pack)
                pack_unit = 'Strips'
                base_unit_display = 'Tablets'
            else:
                base_unit_qty = int(pack_qty)  
                pack_unit = unit_type.capitalize() + 's' if unit_type not in ['MISCELLANEOUS', 'SYRUP', 'OINTMENT'] else unit_type.capitalize()
                base_unit_display = pack_unit
            
            expired_list.append({
                'name': name,
                'batch_number': batch_number,  
                'date_received': date_received,
                'pack_qty': pack_qty,
                'base_unit_qty': base_unit_qty,
                'expiry_date': expiry_date_str,
                'pack_unit': pack_unit,
                'base_unit_display': base_unit_display
            })
        return expired_list
        
    def get_returnable_batches(self):
        """Retrieves active batches that are expired, or expiring in the next 90 days (approx. 3 months)."""
        if not self.conn: return []
        
        # MODIFIED: Removed p.cost_price from SELECT
        query = """
        SELECT  
            T2.batch_id, T1.product_id, T1.name, T1.supplier, T2.date_received,  
            T2.expiry_date, T2.stock_quantity, T2.pack_cost_price, T1.units_per_pack, T1.unit_type, T2.batch_number
        FROM products AS T1
        JOIN stock_batches AS T2 ON T1.product_id = T2.product_id
        WHERE T2.stock_quantity > 0 AND T2.expiry_date <= STRFTIME('%Y-%m', 'now', '+90 days')
        ORDER BY T1.supplier ASC, T2.expiry_date ASC;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
        
    def add_supplier_name(self, name):
        """Inserts a new supplier name if it doesn't exist."""
        if not self.conn: return False
        try:
            with self.conn:
                self.cursor.execute("INSERT OR IGNORE INTO suppliers (name) VALUES (?)", (name,))
                return True
        except sqlite3.Error as e:
            print(f"Error adding supplier: {e}")
            return False

    def get_company_names(self):
        """Retrieves all unique company names."""
        if not self.conn: return []
        self.cursor.execute("SELECT name FROM companies ORDER BY name ASC")
        return [row[0] for row in self.cursor.fetchall()]

    def add_company_name(self, name):
        """Inserts a new company name if it doesn't exist."""
        if not self.conn: return False
        try:
            with self.conn:
                self.cursor.execute("INSERT OR IGNORE INTO companies (name) VALUES (?)", (name,))
                return True
        except sqlite3.Error as e:
            print(f"Error adding company: {e}")
            return False

    def get_product_names(self):
        if not self.conn: return []
        self.cursor.execute("SELECT name FROM products ORDER BY name ASC")
        return [row[0] for row in self.cursor.fetchall()]

    def get_product_stock_by_name(self, product_name):
        """Retrieves total active stock (packs) for a given product name. (MODIFIED)"""
        if not self.conn: return None
        
        # Prices are now dynamic per batch, so only return stock quantity and unit information.
        query = """
        SELECT 
            COALESCE(SUM(b.stock_quantity), 0.0), 
            p.units_per_pack, 
            p.unit_type
        FROM products p
        LEFT JOIN stock_batches b ON p.product_id = b.product_id AND b.expiry_date >= STRFTIME('%Y-%m', 'now')
        WHERE p.name = ?
        GROUP BY p.product_id;
        """
        self.cursor.execute(query, (product_name,))
        return self.cursor.fetchone()


    def get_dashboard_data(self):
        """Fetches consolidated data for the dashboard. UPDATED for dynamic inventory valuation."""
        if not self.conn: return {
            'inventory_value': 0.0, 'low_stock_count': 0, 'expired_count': 0,
            'near_expiry_count': 0, 'last_7_days_transactions': 0, 'last_7_days_revenue': 0.0,
        }
        
        # 1. Total Inventory Cost Value (NOW uses batch cost price)
        self.cursor.execute("""
            SELECT COALESCE(SUM(b.stock_quantity * b.pack_cost_price), 0.0)    
            FROM stock_batches b
            WHERE b.stock_quantity > 0 AND b.expiry_date >= STRFTIME('%Y-%m', 'now');
        """)
        total_inventory_value = self.cursor.fetchone()[0] or 0.0
        
        # 2. Total Low Stock Items (Below Reorder Point)
        self.cursor.execute("""
            WITH CurrentStock AS (
                SELECT product_id, SUM(stock_quantity) AS TotalStock
                FROM stock_batches
                WHERE expiry_date >= STRFTIME('%Y-%m', 'now')
                GROUP BY product_id
            )
            SELECT COUNT(p.product_id)
            FROM products p
            LEFT JOIN CurrentStock cs ON p.product_id = cs.product_id
            WHERE COALESCE(cs.TotalStock, 0.0) <= p.reorder_point;
        """)
        low_stock_count = self.cursor.fetchone()[0] or 0
        
        # 3. Sales/Revenue for the Last 7 Days (Excluding Voided Sales)
        seven_days_ago = (datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        self.cursor.execute("""
            SELECT COUNT(id), COALESCE(SUM(total_amount), 0.0)
            FROM sales
            WHERE DATE(transaction_date) >= ? AND status = 'Finalized';
        """, (seven_days_ago,))
        last_7_days_sales = self.cursor.fetchone()
        last_7_days_transactions = last_7_days_sales[0]
        last_7_days_revenue = last_7_days_sales[1]
        
        # 4. Expiry Alerts (Counts only)
        alerts = self.get_expiry_alerts()
        expired_count = len(alerts['expired'])
        near_expiry_count = len(alerts['1_month']) + len(alerts['2_month'])
        
        return {
            'inventory_value': total_inventory_value,
            'low_stock_count': low_stock_count,
            'expired_count': expired_count,
            'near_expiry_count': near_expiry_count,
            'last_7_days_transactions': last_7_days_transactions,
            'last_7_days_revenue': last_7_days_revenue,
        }
        
    def perform_daily_backup(self):
        """Creates a timestamped backup file in a 'backups' directory and cleans up old files."""
        if not self.conn: return False, "Database connection is not active."
        
        backup_dir = "backups"
        
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # 1. CREATE NEW BACKUP
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        backup_filename = os.path.join(backup_dir, f"pharmacy_pos_backup_{timestamp_str}.db")
        
        try:
            self.conn.close() 
            shutil.copyfile(self.db_name, backup_filename)
            self.connect() 
            
            print(f"✅ Auto-Backup successful: {backup_filename}")
            
            # --- RUN RETENTION POLICY ---
            self._cleanup_old_backups(backup_dir)
            # --------------------------
            
            return True, backup_filename
        
        except Exception as e:
            self.connect() 
            print(f"❌ Auto-Backup failed: {e}")
            return False, str(e)

    def _cleanup_old_backups(self, backup_dir):
        """Implements a GFS-style daily/weekly/monthly retention policy."""
        
        today = datetime.date.today()
        all_backups = []

        for filename in os.listdir(backup_dir):
            if filename.endswith(".db") and filename.startswith("pharmacy_pos_backup_"):
                try:
                    date_part = filename.split('_')[3]
                    time_part = filename.split('_')[4].split('.')[0]
                    
                    file_datetime = datetime.datetime.strptime(date_part + time_part, "%Y%m%d%H%M")
                    all_backups.append({'filename': filename, 'date': file_datetime.date()})
                except Exception as e:
                    continue

        all_backups.sort(key=lambda x: x['date'])
        
        files_to_keep = set()
        
        # Policy 1: Keep all files from the last 7 days
        seven_days_ago = today - datetime.timedelta(days=7)
        for backup in all_backups:
            if backup['date'] >= seven_days_ago:
                files_to_keep.add(backup['filename'])
        
        # Policy 2: Keep the last backup of each previous full week (Weeks 2-5)
        weekly_keep_map = {}  
        relevant_backups = [b for b in all_backups if b['date'] < seven_days_ago]  

        for backup in relevant_backups:
            week_key = f"{backup['date'].isocalendar()[0]}-{backup['date'].isocalendar()[1]}"
            weekly_keep_map[week_key] = backup['filename']

        sorted_weekly_backups = sorted(weekly_keep_map.values(), key=lambda f: datetime.datetime.strptime(f.split('_')[3], "%Y%m%d"), reverse=True)
        for filename in sorted_weekly_backups[:4]: 
             files_to_keep.add(filename)


        # Policy 3: Keep the oldest backup of each previous full month (Last 12 months)
        monthly_keep_map = {} 

        for backup in all_backups:
            month_key = f"{backup['date'].year}-{backup['date'].month}"
            
            if month_key not in monthly_keep_map:
                monthly_keep_map[month_key] = backup['filename']
        
        sorted_monthly_backups = sorted(monthly_keep_map.values(), key=lambda f: datetime.datetime.strptime(f.split('_')[3], "%Y%m%d"), reverse=True)
        for filename in sorted_monthly_backups[:12]:    
            files_to_keep.add(filename)
        
        
        # Final Deletion
        deleted_count = 0
        total_count = len(all_backups)
        
        for backup in all_backups:
            if backup['filename'] not in files_to_keep:
                try:
                    os.remove(os.path.join(backup_dir, backup['filename']))
                    deleted_count += 1
                except OSError:
                    pass    

        if deleted_count > 0:
            print(f"🧹 Backup Cleanup: Deleted {deleted_count} old backup files (Total remaining: {total_count - deleted_count}).")

    def get_doctor_names(self):
        """Retrieves all unique doctor names."""
        if not self.conn: return []
        self.cursor.execute("SELECT name FROM doctors ORDER BY name ASC")
        return [row[0] for row in self.cursor.fetchall()]
    
    # --- SALES & RETURN OVERRIDES (Unchanged) ---
    # ... (omitted for brevity, assume unchanged)

    def get_sale_header_data(self, sale_id):
        """Retrieves key header data for a single sale."""
        if not self.conn: return None
        try:
            self.cursor.execute("SELECT transaction_date, total_amount, discount, patient_name, doctor_ref, status FROM sales WHERE id = ?", (sale_id,))
            header_data = self.cursor.fetchone()
            if not header_data:
                return None
                
            date_time, total_amount, discount, patient_name, doctor_ref, status = header_data
            
            # Calculate Subtotal (since total_amount is the net amount after discount)
            subtotal = total_amount + discount
            
            return {
                'date': date_time.split(' ')[0], 
                'subtotal': subtotal,
                'discount': discount,
                'final_total': total_amount,
                'patient_name': patient_name or 'CASH SALES',
                'doctor_ref': doctor_ref or 'N/A',
                'status': status
            }
        except sqlite3.Error as e:
            print(f"Error fetching sale header: {e}")
            return None

    def add_doctor_name(self, name):
        """Inserts a new doctor name if it doesn't exist."""
        if not self.conn: return False
        try:
            with self.conn:
                self.cursor.execute("INSERT OR IGNORE INTO doctors (name) VALUES (?)", (name,))
                return True
        except sqlite3.Error as e:
            print(f"Error adding doctor: {e}")
            return False

    # >>> ADDED: Supplier Master Management Methods <<<
    def get_all_suppliers_master(self):
        """Retrieves all suppliers and their contact info."""
        if not self.conn: return []
        query = """
        SELECT
            T1.supplier_name, T1.contact_person, T1.phone, T1.email, T1.address
        FROM supplier_contact AS T1
        ORDER BY T1.supplier_name ASC;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def add_or_update_supplier_master(self, name, contact_person, phone, email, address):
        """Inserts a new supplier or updates an existing one."""
        if not self.conn: return False, "DB connection inactive."
        try:
            with self.conn:
                # Also ensure the name is in the base `suppliers` table for complter
                self.cursor.execute("INSERT OR IGNORE INTO suppliers (name) VALUES (?)", (name,))
                
                self.cursor.execute("""
                    INSERT INTO supplier_contact (supplier_name, contact_person, phone, email, address)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(supplier_name) DO UPDATE SET
                        contact_person = excluded.contact_person,
                        phone = excluded.phone,
                        email = excluded.email,
                        address = excluded.address
                """, (name, contact_person, phone, email, address))
            return True, "Supplier contact saved successfully."
        except sqlite3.Error as e:
            print(f"Error adding/updating supplier master: {e}")
            return False, f"Database Error: {e}"

    def delete_supplier_master(self, supplier_name):
        """
        Deletes a supplier from the master list (and base table) only if they have 
        NO records in the purchase_orders table.
        """
        if not self.conn: return False, "DB connection inactive."
        
        # 1. Check for dependencies in purchase_orders
        self.cursor.execute("SELECT COUNT(*) FROM purchase_orders WHERE supplier_name = ?", (supplier_name,))
        po_count = self.cursor.fetchone()[0]
        
        if po_count > 0:
            return False, f"Cannot delete '{supplier_name}'. It is linked to {po_count} existing Purchase Order(s) and must be kept for auditing."
        
        try:
            with self.conn:
                # 2. Delete from supplier_contact (Master List)
                self.cursor.execute("DELETE FROM supplier_contact WHERE supplier_name = ?", (supplier_name,))
                
                # 3. Delete from base suppliers table (used for simple lookups/completions)
                self.cursor.execute("DELETE FROM suppliers WHERE name = ?", (supplier_name,))

            return True, f"Supplier '{supplier_name}' successfully deleted."
        except sqlite3.Error as e:
            print(f"Error deleting supplier master: {e}")
            return False, f"Database Error: {e}"

            
    def get_supplier_transaction_summary(self, supplier_name):
        """Retrieves all POs, Payments, and Returns for a given supplier."""
        if not self.conn: return {'orders': [], 'payments': [], 'returns': []}

        # 1. Orders
        self.cursor.execute("""
            SELECT order_id, invoice_number, order_date, total_invoice_amount, status
            FROM purchase_orders WHERE supplier_name = ?
            ORDER BY order_date DESC
        """, (supplier_name,))
        orders = self.cursor.fetchall()
        
        # 2. Payments (must join to get payment details)
        self.cursor.execute("""
            SELECT T1.payment_id, T1.payment_date, T1.amount_paid, T1.payment_method, T1.order_id
            FROM supplier_payments AS T1
            LEFT JOIN purchase_orders AS T2 ON T1.order_id = T2.order_id
            WHERE T2.supplier_name = ? 
            ORDER BY T1.payment_date DESC
        """, (supplier_name,))
        payments = self.cursor.fetchall()
        
        # 3. Returns (Supplier Returns acting as credit notes)
        self.cursor.execute("""
            SELECT return_date, total_refund_value, reason, order_id
            FROM returns 
            WHERE supplier_name = ? AND reason NOT LIKE 'Customer Return%'
            ORDER BY return_date DESC
        """, (supplier_name,))
        returns = self.cursor.fetchall()

        return {'orders': orders, 'payments': payments, 'returns': returns}
        
    def get_supplier_product_history(self, supplier_name):
        """
        Retrieves a distinct list of products ordered from a supplier, along with the 
        latest cost price and last order date for each product.
        """
        if not self.conn: return []
        
        # This complex query uses nested subqueries to find the latest data points 
        # for *each distinct product* from the purchase history of the specified supplier.
        query = """
        WITH SupplierPOs AS (
            SELECT order_id FROM purchase_orders WHERE supplier_name = ?
        ),
        ProductOrderData AS (
            SELECT
                pi.product_id,
                pi.pack_cost_price,
                po.order_date,
                ROW_NUMBER() OVER(PARTITION BY pi.product_id ORDER BY po.order_date DESC, pi.p_item_id DESC) as rn
            FROM purchase_items pi
            JOIN SupplierPOs spo ON pi.order_id = spo.order_id
            JOIN purchase_orders po ON po.order_id = spo.order_id
        )
        SELECT DISTINCT
            p.product_id,
            p.name,
            p.unit_type,
            c.name AS class_name,
            pod.pack_cost_price,
            pod.order_date
        FROM products p
        JOIN ProductOrderData pod ON p.product_id = pod.product_id
        LEFT JOIN classes c ON p.class_id = c.class_id
        WHERE pod.rn = 1
        ORDER BY pod.order_date DESC;
        """
        self.cursor.execute(query, (supplier_name,))
        return self.cursor.fetchall()


    # >>> ADDED: Methods for PO Viewer Dialog <<<

    def get_po_details_for_viewer(self, order_id):
        """Fetches full header and line item details for a Purchase Order."""
        
        # 1. Fetch Header Details
        self.cursor.execute("""
            SELECT 
                supplier_name, invoice_number, invoice_date, status, total_invoice_amount
            FROM purchase_orders 
            WHERE order_id = ?
        """, (order_id,))
        header_data = self.cursor.fetchone()
        
        if not header_data:
            return None

        header = {
            'supplier_name': header_data[0],
            'invoice_number': header_data[1],
            'invoice_date': header_data[2],
            'status': header_data[3],
            'total_invoice_amount': header_data[4]
        }

        # 2. Fetch Line Items Details (using pack_quantity_ordered and pack_cost_price)
        self.cursor.execute("""
            SELECT 
                T1.p_item_id, T2.name AS product_name, T1.batch_number, T1.pack_quantity_ordered, T1.pack_cost_price, 
                T1.pack_quantity_ordered * T1.pack_cost_price AS line_total, T2.units_per_pack, T3.expiry_date
            FROM purchase_items T1
            LEFT JOIN products T2 ON T1.product_id = T2.product_id
            LEFT JOIN stock_batches T3 ON T1.p_item_id = T3.purchase_item_id
            WHERE T1.order_id = ?
            ORDER BY T2.name
        """, (order_id,))
        
        items = []
        for row in self.cursor.fetchall():
            items.append({
                'p_item_id': row[0],
                'product_name': row[1],
                'batch_number': row[2],
                'pack_quantity': row[3],
                'pack_cost': row[4],
                'line_total': row[5],
                'units_per_pack': row[6],
                'expiry_date': row[7]
            })

        return {'header': header, 'items': items}

    def get_active_stock_for_purchase_item(self, p_item_id):
        """Calculates the remaining stock quantity for a specific purchase item ID (from batches)."""
        self.cursor.execute("""
            SELECT COALESCE(SUM(stock_quantity), 0.0) 
            FROM stock_batches 
            WHERE purchase_item_id = ? AND expiry_date >= STRFTIME('%Y-%m', 'now')
        """, (p_item_id,))
        return self.cursor.fetchone()[0]

    # >>> NEW: Settings Management Methods <<<
    def get_setting(self, key, default=None):
        """Retrieves a single configuration setting."""
        if not self.conn: return default
        self.cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        result = self.cursor.fetchone()
        return result[0] if result else default

    def save_setting(self, key, value):
        """Inserts or updates a single configuration setting."""
        if not self.conn: return False
        try:
            # Convert value to string for storage
            str_value = str(value)
            with self.conn:
                self.cursor.execute(
                    "INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                    (key, str_value)
                )
            return True
        except sqlite3.Error as e:
            print(f"Error saving setting {key}: {e}")
            return False

    def close(self):
        if self.conn:
            self.conn.close()

# ==============================================================================
# UTILITY FUNCTION: NUMBER TO WORDS (UNCHANGED)
# ==============================================================================

def number_to_words(number):
    """
    Converts a number to words (RUPEES ONLY, no decimal/paise) and attempts 
    to split the result into two lines if the total word count exceeds 8.
    """
    if number < 0:
        return "MINUS " + number_to_words(abs(number))
    
    whole_part = int(number)
    
    units = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
    teens = ["TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"]
    tens = ["", "", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]

    def _convert_below_1000(n):
        if n == 0: return ""
        if n < 10: return units[n]
        if n < 20: return teens[n - 10]
        if n < 100:
            return tens[n // 10] + (" " + units[n % 10] if n % 10 != 0 else "")
        return units[n // 100] + " HUNDRED" + (" AND " + _convert_below_1000(n % 100) if n % 100 != 0 else "")

    def _convert(n):
        if n == 0: return "ZERO"
        words = _convert_below_1000(n % 1000)
        n //= 1000
        if n > 0:
            words = _convert_below_1000(n % 1000) + " THOUSAND " + (" " + words if words else "")
            n //= 1000
            if n > 0:
                words = _convert_below_1000(n % 1000) + " MILLION " + (" " + words if words else "")
        return words.strip()

    whole_words = _convert(whole_part)
    
    if whole_words == "ZERO":
        result = "ZERO RUPEES ONLY"
    else:
        result = whole_words + " RUPEES ONLY"

    # --- Line Break Logic ---
    parts = result.split()
    if len(parts) > 8:
        # Attempt to split roughly in half, focusing on a clean break after a major unit (THOUSAND, HUNDRED)
        split_index = len(parts) // 2
        
        # Look for a clean break near the middle
        for i in range(split_index, 0, -1):
            if parts[i].upper() in ["THOUSAND", "HUNDRED", "MILLION", "RUPEES"]:
                split_index = i + 1
                break
        
        line1 = " ".join(parts[:split_index])
        line2 = " ".join(parts[split_index:])
        return f"{line1}\n{line2}"
        
    return result

# ... (After number_to_words function)

# ==============================================================================
# UTILITY FUNCTION: PDF FILE MANAGEMENT (NEW)
# ==============================================================================

# ==============================================================================
# UTILITY FUNCTION: PDF FILE MANAGEMENT (MODIFIED FOR RELIABLE PRINTING)
# ==============================================================================

# --- CRITICAL FIX: Ensure assets are found when bundled by PyInstaller ---
def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Use the function to define the logo path for the EXE
LOGO_FILE_PATH = get_resource_path("logo.png")
# --- END CRITICAL FIX ---

LOGO_WATERMARK_SIZE = 100 * mm
DOWNWARD_SHIFT = 10 * mm

def _get_save_path(invoice_id, invoice_date_str, is_reprint=False):
    """
    Constructs the dynamic save path (./Bills/YYYY/MM/DD) and ensures the directory exists.
    Returns the full filename including the path.
    """
    try:
        if invoice_id == 'PREVIEW':
            # Previews go directly into a 'Temp' folder to avoid cluttering the date structure
            date_obj = datetime.date.today()
            date_part = date_obj.strftime("%Y%m%d")
            time_part = datetime.datetime.now().strftime('%H%M%S')
            
            base_dir = os.path.join("Bills", "Temp")
            filename = f"Preview_Invoice_{invoice_id}_{date_part}_{time_part}.pdf"
        else:
            # Note: POS transactions store datetime, but we extract the date part first.
            if len(invoice_date_str) > 10:
                date_part_str = invoice_date_str.split(' ')[0]
            else:
                date_part_str = invoice_date_str

            date_obj = datetime.datetime.strptime(date_part_str, '%Y-%m-%d').date()
            
            year_folder = date_obj.strftime('%Y')
            month_folder = date_obj.strftime('%m - %B')
            day_folder = date_obj.strftime('%d')
            
            # Construct the nested folder path: Bills/YYYY/MM - Month/DD
            base_dir = os.path.join("Bills", year_folder, month_folder, day_folder)
            
            # Use original transaction date for finalized invoices
            date_part = date_obj.strftime('%Y%m%d') 
            
            filename_prefix = "REPRINT_" if is_reprint else ""
            
            # Use current time in case multiple reprints happen on the same day for unique naming
            timestamp = datetime.datetime.now().strftime('_%H%M%S') if is_reprint else ""
            
            filename = f"{filename_prefix}Invoice_{invoice_id}_{date_part}{timestamp}.pdf"

        # Create the directory if it doesn't exist
        os.makedirs(base_dir, exist_ok=True)
        
        return os.path.join(base_dir, filename)

    except Exception as e:
        print(f"Error generating save path: {e}. Falling back to root directory.")
        return f"Invoice_{invoice_id}.pdf"

def generate_2bills_pdf(data, filename):
    """
    Generates 2 bills (Customer & Office copy) side-by-side with a translucent, 
    centered logo watermark, incorporating the specific column shift.
    """
    pdf = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    half_width = width / 2
    half_height = height / 2
    
    # Shop Details (Local constants for PDF generation)
    SHOP_NAME = "SHREE RAM MEDICAL"
    SHOP_ADDRESS = "Bus Stand Kamtha(BK), Tq Ardhapur, Dist Nanded - 431704"
    SHOP_DL_NO = "DL No: 20*346101 / 21*346102"
    SHOP_FSSAI = "FSSAI: 21521236000113"
    SHOP_PHONE = "Phone: 9822549178"
    
    # --- NEW TERMS & CONDITIONS ---
    TERMS_LINE1 = "Goods once sold will not be taken back or exchanged"
    TERMS_LINE2 = "All disputes subject to jursdiction only"
    # ----------------------------

    # Define Column Widths for a single bill (in ReportLab points)
    bill_width = half_width - 10 * mm
    
    # 🚨 BATCH COLUMN SHIFT LOGIC (3mm left shift)
    COL_SHIFT = 3 * mm 

    # NOTE: The width taken from Index 3 (Rate) is given to Index 4 (Batch) to maintain 
    # the correct total table width, simulating a negative offset for the Batch content.
    col_widths = [
        0.30 * bill_width,                  # Product (Index 0)
        0.06 * bill_width,                  # Mfg (Manufacturer/Company) (Index 1) 
        0.08 * bill_width,                  # Qty (Index 2) 
        0.11 * bill_width - COL_SHIFT,      # 🚨 Rate (Index 3) - REDUCED width to push Batch left
        0.23 * bill_width + COL_SHIFT,      # 🚨 Batch (Index 4) - INCREASED width to compensate
        0.01 * bill_width,                  # Exp. (Index 5)
        0.21 * bill_width                   # Amt. (Index 6)
    ]
    
    MAX_PROD_WIDTH = col_widths[0] - 1 * mm
    
    # Vertical spacing constants (optimized)
    LINE_H = 4 * mm           
    TABLE_LINE_H = 3.5 * mm
    
    # Maximum rows to print
    MAX_ROWS = 20
    
    # Space reserved at the bottom for Totals/Payment/Signature
    TOTALS_BLOCK_HEIGHT = 18 * mm 
    
    # Vertical shift constants
    SHIFT_UP = 12.5 * mm
    ADDITIONAL_FOOTER_SHIFT = 10 * mm 
    
    # --- CONSTANTS FOR TIGHTER PADDING ---
    PADDING_AMOUNT_TO_LINE = 2 * mm 
    PADDING_LINE_TO_TC = 3 * mm
    # -----------------------------------------

    # Define the horizontal shift for the signature text
    SIGNATURE_X_OFFSET = 5 * mm 

    def _draw_watermark_image(x_center_bill, y_center_bill):
        
        box_height = height / 2 - 2 * 5 * mm 
        
        y_content_top = y_center_bill + box_height
        y_content_bottom = y_center_bill + (5 * mm) + TOTALS_BLOCK_HEIGHT 
        
        img_x_center = x_center_bill + bill_width / 2
        img_y_center = (y_content_top + y_content_bottom) / 2
        
        if not os.path.exists(LOGO_FILE_PATH):
            pdf.saveState()
            pdf.setFillColor(colors.lightgrey) 
            pdf.setFont('Helvetica-Bold', 12)
            pdf.drawCentredString(img_x_center, img_y_center, "[NO LOGO]")
            pdf.restoreState()
            return

        try:
            pdf.saveState()
            
            img_x_start = img_x_center - LOGO_WATERMARK_SIZE / 2
            
            # Calculate vertical start position (top-left corner of the image)
            img_y_start = img_y_center - LOGO_WATERMARK_SIZE / 2 
            
            # 🆕 APPLY DOWNWARD SHIFT
            img_y_start -= DOWNWARD_SHIFT
            
            pdf.drawImage(
                LOGO_FILE_PATH,
                img_x_start,
                img_y_start,
                width=LOGO_WATERMARK_SIZE, 
                height=LOGO_WATERMARK_SIZE,
                mask='auto'
            )
            
            pdf.restoreState()

        except Exception as e:
            print(f"Error drawing large watermark image: {e}")
            pdf.saveState()
            pdf.setFillColor(colors.lightgrey) 
            pdf.setFont('Helvetica-Bold', 12)
            pdf.drawCentredString(img_x_center, img_y_center, "[ERROR]")
            pdf.restoreState()


    def draw_single_bill(x_offset, y_offset, title):
        margin = 5 * mm 
        box_width = half_width - 2 * margin
        box_height = height / 2 - 2 * margin 
        
        start_x = x_offset + margin
        start_y = y_offset + margin 
        
        # --- WATERMARK CALL ---
        _draw_watermark_image(start_x, start_y)
        # ----------------------

        # --- Fixed Coordinates ---
        X_LEFT = start_x + 2 * mm
        X_RIGHT = start_x + box_width - 5.5 * mm 
        X_TOTAL_LABEL_END = start_x + box_width - col_widths[6] - 4 * mm
        
        X_SIGNATURE_ANCHOR = X_TOTAL_LABEL_END - SIGNATURE_X_OFFSET 

        # --- Header & Shop Info (Condensed) ---
        y = start_y + box_height
        y_top = y
        
        pdf.setFont("Helvetica-Bold", 9)
        y -= 4 * mm
        pdf.drawCentredString(start_x + box_width / 2, y, SHOP_NAME)

        pdf.setFont("Helvetica", 5.5) 
        y -= 3 * mm
        pdf.drawCentredString(start_x + box_width / 2, y, SHOP_ADDRESS)
        
        pdf.setFont("Helvetica", 6.0)
        y -= 4 * mm
        pdf.drawCentredString(start_x + box_width / 2, y, f"{SHOP_DL_NO} | {SHOP_FSSAI} | {SHOP_PHONE}")
        
        y -= 1.5 * mm
        pdf.setLineWidth(0.3)
        pdf.line(start_x + 2*mm, y, start_x + box_width - 2*mm, y)
        y -= LINE_H - 1 * mm

        # --- Patient Info (Tight alignment) ---
        original_date_formatted = datetime.datetime.strptime(data['print_date'], '%Y-%m-%d').strftime('%d-%m-%Y')
        
        pdf.setFont("Helvetica-Bold", 7)
        pdf.drawString(X_LEFT, y, f"Cash Memo ({title} Copy)")
        
        y -= LINE_H
        pdf.setFont("Helvetica", 6.5)
        pdf.drawString(X_LEFT, y, f"Patient: {data.get('patient_name', 'CASH SALES')}")
        pdf.drawRightString(X_RIGHT, y, f"Memo No: {data['sale_id']}")
        
        y -= LINE_H
        pdf.drawString(X_LEFT, y, f"Address: {data.get('patient_address', 'N/A')}")
        pdf.drawRightString(X_RIGHT, y, f"Date: {original_date_formatted}") 
        
        y -= LINE_H
        pdf.drawString(X_LEFT, y, f"Doctor: {data.get('doctor_ref', 'N/A')}")
        
        y -= 1.5 * mm
        pdf.setLineWidth(0.3)
        pdf.line(start_x + 2*mm, y, start_x + box_width - 2*mm, y)
        y -= 1.5 * mm

        # --- Table Headers ---
        headers = ["Product", "Mfg", "Qty", "Rate", "Batch", "Exp.", "Amt."] 
        header_y = y - 3 * mm
        
        pdf.setFont("Helvetica-Bold", 6.5)
        x = start_x + 2*mm
        
        for i, h in enumerate(headers):
            if i == 6:  
                pdf.drawRightString(X_RIGHT, header_y, h)
            elif i in [2, 3, 5]: 
                pdf.drawRightString(x + col_widths[i] - 1*mm, header_y, h)
            elif i == 4: 
                # 🚨 BATCH HEADER SHIFTED LEFT
                pdf.drawCentredString(x + col_widths[i] / 2 - COL_SHIFT, header_y, h)
            else: 
                pdf.drawString(x, header_y, h)
            x += col_widths[i]
            
        pdf.setLineWidth(0.3)
        pdf.line(start_x + 2*mm, header_y - 1.5*mm, start_x + box_width - 2*mm, header_y - 1.5*mm)

        # --- Table Rows ---
        pdf.setFont("Helvetica", 6.5)
        row_y = header_y - 1.5*mm - TABLE_LINE_H 
        
        x_positions = []
        current_x = start_x + 2*mm
        for w in col_widths:
            x_positions.append(current_x)
            current_x += w
            
        MAX_PROD_WIDTH_TEXT = pdf.stringWidth("A", "Helvetica", 6.5) * 15 

        for i in range(MAX_ROWS):
            if i < len(data["items"]):
                row = data["items"][i]
            else:
                break 

            for j, val in enumerate(row):
                val_str = str(val)
                
                if j == 0: 
                    prod_name_width = pdf.stringWidth(val_str, "Helvetica", 6.5)
                    if prod_name_width > MAX_PROD_WIDTH:
                        while pdf.stringWidth(val_str + '...', "Helvetica", 6.5) > MAX_PROD_WIDTH:
                            val_str = val_str[:-1]
                        val_str += '...'
                    pdf.drawString(x_positions[j], row_y, val_str)
                elif j == 1: 
                    pdf.drawString(x_positions[j], row_y, val_str)
                elif j == 2: 
                    pdf.drawRightString(x_positions[j] + col_widths[j] - 1*mm, row_y, val_str)
                elif j == 3: 
                    pdf.drawRightString(x_positions[j] + col_widths[j] - 1*mm, row_y, val_str)
                elif j == 5:
                    if '/' in val_str:
                        display_exp = val_str.split('/')[0] + '/' + val_str.split('/')[1][-2:]
                    else:
                        display_exp = val_str
                    pdf.drawRightString(x_positions[j] + col_widths[j] - 1*mm, row_y, display_exp)
                elif j == 6:
                    pdf.drawRightString(X_RIGHT, row_y, val_str)
                elif j == 4:
                    # 🚨 BATCH CONTENT SHIFTED LEFT
                    pdf.drawCentredString(x_positions[j] + col_widths[j] / 2 - COL_SHIFT, row_y, val_str)

            row_y -= TABLE_LINE_H
            
        # --- Footer separator and Totals ---
        y_footer_start_divider = start_y + 19 * mm + SHIFT_UP
        pdf.setLineWidth(0.3)
        pdf.line(start_x + 2*mm, y_footer_start_divider, start_x + box_width - 2*mm, y_footer_start_divider)

        y_total_num_block = start_y + 12 * mm + SHIFT_UP
        
        pdf.setFont("Helvetica", 6)
        y_subtotal = y_total_num_block + 4*mm
        pdf.drawRightString(X_TOTAL_LABEL_END, y_subtotal, "Subtotal:")
        pdf.setFont("Helvetica-Bold", 6.5)
        pdf.drawRightString(X_RIGHT, y_subtotal, data["total_amount"])
        
        y_discount = y_subtotal - 4*mm
        pdf.setFont("Helvetica", 6)
        pdf.drawRightString(X_TOTAL_LABEL_END, y_discount, "Discount:")
        pdf.setFont("Helvetica-Bold", 6.5)
        pdf.drawRightString(X_RIGHT, y_discount, data["discount"])

        y_grand_total = y_discount - 4*mm
        pdf.setFont("Helvetica-Bold", 6.5)
        pdf.drawRightString(X_TOTAL_LABEL_END, y_grand_total, "GRAND TOTAL:")
        pdf.drawRightString(X_RIGHT, y_grand_total, data["grand_total"])

        pdf.setFont("Helvetica", 6.5)
        y_payment = y_subtotal
        pdf.drawString(X_LEFT, y_payment, f"Payment: {data['payment_method']}")
        
        amount_in_words = data['amount_in_words'].split('\n')
        pdf.setFont("Helvetica", 5.5) 
        y_words_line1 = y_payment - 4*mm
        pdf.drawString(X_LEFT, y_words_line1, f"In words: {amount_in_words[0]}")

        if len(amount_in_words) > 1:
            y_words_line2 = y_words_line1 - 4*mm
            pdf.drawString(X_LEFT, y_words_line2, amount_in_words[1])
        
        y_new_divider = y_grand_total - PADDING_AMOUNT_TO_LINE 
        pdf.setLineWidth(0.3)
        pdf.line(start_x + 2*mm, y_new_divider, start_x + box_width - 2*mm, y_new_divider)
        
        y_terms_header_base = start_y + 6.5 * mm + ADDITIONAL_FOOTER_SHIFT 
        y_signature_title = y_terms_header_base
        y_text_block_base_target = y_new_divider - PADDING_LINE_TO_TC
        TEXT_BLOCK_V_OFFSET_NEEDED = y_terms_header_base - y_text_block_base_target
        
        X_SIGNATURE_ANCHOR = X_TOTAL_LABEL_END - SIGNATURE_X_OFFSET 
        y_signature_title_new = y_signature_title - TEXT_BLOCK_V_OFFSET_NEEDED
        pdf.setFont("Helvetica-Bold", 6)
        pdf.drawString(X_SIGNATURE_ANCHOR, y_signature_title_new, "For Q.P. Sign") 
        
        y_signature_new = start_y + 1 * mm + ADDITIONAL_FOOTER_SHIFT - TEXT_BLOCK_V_OFFSET_NEEDED
        pdf.setFont("Helvetica", 6)
        pdf.drawString(X_SIGNATURE_ANCHOR, y_signature_new, "Signature")

        y_terms_header_new = y_signature_title_new
        pdf.setFont("Helvetica-Bold", 6)
        pdf.drawString(X_LEFT, y_terms_header_new, "Terms & Conditions:")
        
        y_terms_line1_new = y_terms_header_new - 3 * mm
        pdf.setFont("Helvetica", 5.5)
        pdf.drawString(X_LEFT, y_terms_line1_new, TERMS_LINE1)
        
        y_terms_line2_new = y_terms_line1_new - 3 * mm
        pdf.setFont("Helvetica", 5.5)
        pdf.drawString(X_LEFT, y_terms_line2_new, TERMS_LINE2)

        y_lowest_content = min(y_signature_new, y_terms_line2_new)
        FINAL_BOTTOM_MARGIN = 3 * mm 
        y_new_box_bottom = y_lowest_content - FINAL_BOTTOM_MARGIN
        new_box_height = y_top - y_new_box_bottom 
        
        pdf.setStrokeColor(colors.black)
        pdf.setLineWidth(0.6)
        pdf.rect(start_x, y_new_box_bottom, box_width, new_box_height)


    draw_single_bill(0, half_height, "Customer")
    draw_single_bill(half_width, half_height, "Office")

    pdf.setStrokeColor(colors.lightgrey)
    pdf.setLineWidth(0.3)
    pdf.line(5*mm, half_height, width - 5*mm, half_height)
    
    pdf.showPage()
    pdf.save()

# ----------------------------------------------------------------------
# GLOBAL UTILITY FUNCTIONS (OS-NATIVE FILE OPEN)
# ----------------------------------------------------------------------

def _open_file_in_default_viewer(filename):
    """Opens a file using the default system application (for printing/viewing)."""
    if sys.platform.startswith('darwin'):
        # macOS
        subprocess.call(('open', filename))
    elif sys.platform.startswith('win'):
        # Windows (uses the default shell association)
        os.startfile(filename) 
    else:
        # Linux/Unix (uses xdg-open for cross-desktop compatibility)
        try:
            subprocess.call(('xdg-open', filename))
        except FileNotFoundError:
            print("Warning: xdg-open not found. Attempting to open with 'gnome-open'.")
            subprocess.call(('gnome-open', filename))

def _print_pdf_file_consistent(filename, parent_widget):
    """
    Consistent printing function used by both POSWidget and OldBillViewerWidget.
    Opens a file using the default system viewer/printer.
    """
    try:
        _open_file_in_default_viewer(filename)
        
    except Exception as e:
        print(f"❌ Critical error during file open: {e}")
        QMessageBox.critical(parent_widget, "Print Error", 
            f"Failed to open PDF file: {e}\n\nCheck if a PDF reader is installed and configured."
        )

# NOTE: You must also ensure your original functions like 
# _get_save_path and generate_2bills_pdf are present and correct.

# ==============================================================================
# 2. Complete OldBillViewerWidget Class Replacement
# ==============================================================================

# ==============================================================================
# 2. POS WIDGET (THE SALES FRONT-END) - MODIFIED FOR RELIABLE PRINTING
# ==============================================================================

# ==============================================================================
# 2. POS WIDGET (THE SALES FRONT-END) - MODIFIED FOR DIRECT REMOVE BUTTON & DEL KEY
# ==============================================================================

class POSWidget(QWidget):
    
    SHOP_NAME = "SHREE RAM MEDICAL"
    SHOP_ADDRESS = "Bus Stand Kamtha(BK), Tq Ardhapur, Dist Nanded, 431704"
    SHOP_DL_NO = "DL No: 20*346101 / 21*346102"
    SHOP_FSSAI = "FSSAI: 21521236000113"
    SHOP_PHONE = "Phone: 9822549178"
    
    DR_NAME = "DR. Ramesh Mustare"
    
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        
        self.setLayout(QHBoxLayout())
        
        self._setup_autocompleter()
        self._setup_doctor_completer()
        self._setup_transaction_panel()
        self._setup_checkout_panel()
        
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus) # Necessary to receive key events
        
        self.reset_pos_state()

    # ----------------------------------------------------------------------
    # --- MODIFIED Key Press Event Handler (Keeps only DEL key for removal) ---
    # ----------------------------------------------------------------------
    def keyPressEvent(self, event):
        """Handle POS keyboard shortcuts, including Delete key to remove selected item."""
        
        # Ctrl+F: Trigger Refresh/View Sale Preview
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_F:
            self.btn_view_preview.click()
            event.accept()
            return
            
        # Ctrl+P: Trigger Print Last Receipt
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_P:
            self.btn_print_receipt.click()
            event.accept()
            return

        # Ctrl+Enter: Trigger Finalize Sale
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and (event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter):
            self.finalize_button.click()
            event.accept()
            return

        # ESC: Reset State
        if event.key() == Qt.Key.Key_Escape:
            self.reset_pos_state()
            QMessageBox.information(self, "POS Reset", "POS Transaction cleared.")
            self.search_input.setFocus()
            event.accept()
            return

        # 🆕 NEW: Delete Key Logic when table is focused
        if event.key() == Qt.Key.Key_Delete and self.sale_table.hasFocus():
            self._remove_selected_item_via_key()
            event.accept()
            return
            
        super().keyPressEvent(event)

    # ----------------------------------------------------------------------
    # --- Utility Methods ---
    # ----------------------------------------------------------------------

    def reset_pos_state(self):
        # Clear last_sale_data to ensure the 'Print Last Receipt' button is disabled.
        self.current_sale_items = []
        self.last_sale_data = None  
        self.update_sale_table()
        
        self.global_discount_input.setText("0.00")
        self.patient_name_input.clear()
        self.patient_address_input.clear()
        self.doctor_name_input.clear()  
        
        self.btn_view_preview.setEnabled(len(self.current_sale_items) > 0)
        self.finalize_button.setEnabled(False)
        self.btn_print_receipt.setEnabled(False) # Now depends on self.last_sale_data  
        self.receipt_preview_label.setText("Receipt Status: Ready for new sale.\nAdd items to view preview.")
        self.qty_label.setText("Units:")
        self.stock_status_label.setText("Stock: N/A")
        
    def _setup_autocompleter(self):
        product_names = self.db.get_product_names()
        self.completer_model = QStringListModel(product_names)
        self.completer = QCompleter(self.completer_model)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        
    def _setup_doctor_completer(self):
        doctor_names = self.db.get_doctor_names()
        self.doctor_completer_model = QStringListModel(doctor_names)
        self.doctor_completer = QCompleter(self.doctor_completer_model)
        self.doctor_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.doctor_completer.setFilterMode(Qt.MatchFlag.MatchContains)

    def show_completer_on_empty_click(self):
        if not self.search_input.text().strip():
            self.completer.setCompletionPrefix(self.search_input.text())
            self.completer.setFilterMode(Qt.MatchFlag.MatchContains)  
            self.completer.complete()
            
    def _handle_search_return_key(self):
        if self.completer.popup().isVisible():
            top_index = self.completer.completionModel().index(0, 0)
            if top_index.isValid():
                self.completer.popup().setCurrentIndex(top_index)
                completion_text = self.completer.currentCompletion()
                self.search_input.setText(completion_text)
                QApplication.processEvents()  

            self.qty_input.setFocus()
            self.qty_input.selectAll()
        else:
            self._handle_search_return()  

    def _handle_search_return(self):
        product_name = self.search_input.text().strip()
        query = "SELECT product_id FROM products WHERE name = ?"
        self.db.cursor.execute(query, (product_name,))
        
        if self.db.cursor.fetchone():
            self.qty_input.setFocus()  
            self.qty_input.selectAll()
        else:
            QMessageBox.warning(self, "Selection Error", "Product not recognized. Check spelling or try again.")
            self.search_input.setFocus()

    # ----------------------------------------------------------------------
    # --- Core Logic & Data Display Methods ---
    # ----------------------------------------------------------------------
    
    def _run_fefo_fulfillment(self, product_id, qty_base_units_to_sell):
        """
        Retrieves batches and allocates stock, calculating selling/cost price per base unit  
        based on batch data. (UNCHANGED LOGIC)
        """
        query_prod = "SELECT units_per_pack FROM products WHERE product_id = ?"
        self.db.cursor.execute(query_prod, (product_id,))
        units_per_pack = self.db.cursor.fetchone()
        if not units_per_pack: return None
        effective_units_per_pack = units_per_pack[0] if units_per_pack[0] > 0 else 1
        
        query_batches = """
        SELECT batch_id, stock_quantity, pack_selling_price, pack_cost_price
        FROM stock_batches
        WHERE product_id = ? AND stock_quantity > 0 AND expiry_date >= STRFTIME('%Y-%m', 'now')
        ORDER BY expiry_date ASC, date_received ASC
        """
        self.db.cursor.execute(query_batches, (product_id,))
        available_batches = self.db.cursor.fetchall()
        
        if not available_batches: return None
        
        remaining_units_needed = qty_base_units_to_sell
        fulfillment_chunks = []
        
        for batch_data in available_batches:
            if remaining_units_needed <= 0.001: break
                
            batch_id, available_packs, batch_selling_price, batch_cost_price = batch_data  
            available_base_units = available_packs * effective_units_per_pack

            units_to_take = min(remaining_units_needed, available_base_units)
            
            price_per_base_unit = batch_selling_price / effective_units_per_pack if effective_units_per_pack > 0 else batch_selling_price
            cost_per_base_unit = batch_cost_price / effective_units_per_pack if effective_units_per_pack > 0 else batch_cost_price

            if units_to_take > 0:
                fulfillment_chunks.append({
                    'batch_id': batch_id,
                    'qty_base_units': units_to_take,
                    'units_per_pack': effective_units_per_pack,
                    'base_unit_selling_price': price_per_base_unit,
                    'base_unit_cost_price': cost_per_base_unit
                })
                remaining_units_needed -= units_to_take
            
        if remaining_units_needed > 0.001:
            return None
            
        return fulfillment_chunks
        
    def remove_item_by_id(self, product_id_to_remove):
        """Removes all chunks of a product (Legacy fallback)."""
        batches_to_keep = []
        for item in self.current_sale_items:
            if item['product_id'] != product_id_to_remove:
                batches_to_keep.append(item)
            
        self.current_sale_items = batches_to_keep
        self.update_sale_table()  

    def _remove_item_from_sale(self, row):
        """Removes the sale item chunk at the given row index and updates the table."""
        if 0 <= row < len(self.current_sale_items):
            product_name = self.current_sale_items[row]['name']
            del self.current_sale_items[row]
            self.update_sale_table()
            parent_window = self.window()
            if isinstance(parent_window, QMainWindow) and hasattr(parent_window, 'statusBar'):
                parent_window.statusBar.showMessage(f"🗑️ Removed item: {product_name}.", 2000)
                
    def _remove_selected_item_via_key(self):
        """Removes the selected row's item from the current sale (Used by DEL key)."""
        selected_indexes = self.sale_table.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Selection Required", "Please select a row in the table to remove.")
            return

        # Get the row index from the selected item (first selected index)
        row_index = selected_indexes[0].row()
        
        # Use the core removal logic
        self._remove_item_from_sale(row_index)

    def update_quantity_label(self):
        product_name = self.search_input.text().strip()
        
        # --- 1. Get Product Details (Unit Type) ---
        query = "SELECT unit_type, units_per_pack, reorder_point FROM products WHERE name = ?"
        self.db.cursor.execute(query, (product_name,))
        result = self.db.cursor.fetchone()
        
        unit_type = result[0] if result else 'PIECE'
        units_per_pack = result[1] if result else 1
        reorder_point = result[2] if result else 0
        
        label_map = {
            'TABLET': 'Tabs/Units:', 'CAPSULE': 'Capsules/Units:', 'SYRUP': 'Bottles/Units:',  
            'DROP': 'Drops/Units:', 'VIAL': 'Vials/Units:', 'INJECTIBLE': 'Vials/Units:',  
            'SPRAY': 'Units/Cans:', 'POWDER': 'Units/Tins:', 'OINTMENT': 'Tubes/Units:',  
            'MISCELLANEOUS': 'Units:'
        }
        
        placeholder_map = {
            'TABLET': f"Tabs (Max {units_per_pack} per strip)", 'CAPSULE': f"Capsules (Max {units_per_pack} per strip)",  
            'SYRUP': 'Bottles', 'DROP': 'Drops', 'VIAL': 'Vials',  
            'INJECTIBLE': 'Vials', 'SPRAY': 'Cans/Units', 'POWDER': 'Tins/Units',  
            'OINTMENT': 'Tubes/Units', 'MISCELLANEOUS': 'Units'
        }
        
        self.qty_label.setText(label_map.get(unit_type, 'Units:'))
        self.qty_input.setPlaceholderText(placeholder_map.get(unit_type, 'Units'))

        # --- 2. Get Live Stock Information ---
        stock_data = self.db.get_product_stock_by_name(product_name)
        
        if stock_data:
            total_packs, units_per_pack, unit_type = stock_data
            
            if unit_type in ['TABLET', 'CAPSULE']:
                pack_unit_display = 'Strips'
            else:
                pack_unit_display = unit_type.capitalize() + 's' if unit_type not in ['SYRUP', 'OINTMENT', 'MISCELLANEOUS'] else unit_type.capitalize()
            
            total_base_units = int(total_packs * units_per_pack) if units_per_pack > 0 else int(total_packs)
            
            stock_message = f"Stock: {total_packs:.2f} {pack_unit_display} ({total_base_units} units). Reorder: {reorder_point}"
            
            if total_packs <= reorder_point:
                self.stock_status_label.setStyleSheet("font-weight: bold; color: #C82333;") # Red for low stock
            else:
                self.stock_status_label.setStyleSheet("font-weight: normal; color: #343A40;") # Normal color
                
            self.stock_status_label.setText(stock_message)
            
        else:
            self.stock_status_label.setText("Stock: N/A")
            self.stock_status_label.setStyleSheet("font-weight: normal; color: #6C757D;")

    def handle_item_quantity_change(self, item):
        row = item.row()
        col = item.column()
        
        COL_QTY = 4
        COL_UNIT_PRICE = 5
        
        if col not in [COL_QTY, COL_UNIT_PRICE]:
            return  

        try:
            self.sale_table.itemChanged.disconnect()
        except TypeError:
            pass

        try:
            batch_item = self.current_sale_items[row]
            batch_id = batch_item['batch_id']
            
            # 1. Validate and update Quantity
            if col == COL_QTY:
                new_qty = float(self.sale_table.item(row, COL_QTY).text())
                if new_qty <= 0:  
                    self._remove_item_from_sale(row) 
                    return
                
                query = "SELECT T1.stock_quantity, T2.units_per_pack FROM stock_batches AS T1 JOIN products AS T2 ON T1.product_id = T2.product_id WHERE T1.batch_id = ?"
                self.db.cursor.execute(query, (batch_id,))
                stock_data = self.db.cursor.fetchone()
                
                if not stock_data:
                    QMessageBox.critical(self, "Stock Error", "Batch is missing from stock.")
                    self.update_sale_table()
                    return
                    
                stock_packs = stock_data[0]
                units_per_pack = stock_data[1]
                available_base_units = stock_packs * units_per_pack
                
                if new_qty > available_base_units + 0.001:
                    QMessageBox.warning(self, "Stock Error", f"Insufficient stock in batch. Available: {available_base_units:.2f} units.")
                    self.sale_table.item(row, COL_QTY).setText(f"{batch_item['qty_base_units']:.2f}")
                    return
                
                batch_item['qty_base_units'] = new_qty
            
            # 2. Validate and update Unit Price
            elif col == COL_UNIT_PRICE:
                new_price = float(self.sale_table.item(row, COL_UNIT_PRICE).text())
                if new_price <= 0:
                    QMessageBox.warning(self, "Price Error", "Unit Price must be positive.")
                    self.sale_table.item(row, COL_UNIT_PRICE).setText(f"{batch_item['price_per_base_unit']:.2f}")
                    return
                batch_item['price_per_base_unit'] = new_price

            # 3. Recalculate and update Subtotal (Column 7)
            final_subtotal = round(batch_item['price_per_base_unit'] * batch_item['qty_base_units'], 2)
            self.sale_table.setItem(row, 7, QTableWidgetItem(f"{final_subtotal:.2f}"))

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Value must be a valid positive number.")
            self.sale_table.item(row, col).setText(f"{self.current_sale_items[row]['qty_base_units']:.2f}" if col == COL_QTY else f"{self.current_sale_items[row]['price_per_base_unit']:.2f}")
            return
        finally:
            self.sale_table.itemChanged.connect(self.handle_item_quantity_change)
            
        self.update_totals()


    # --- MODIFIED: update_sale_table (Handles column index shift and button) ---
    def update_sale_table(self):
        try:
            self.sale_table.itemChanged.disconnect()
        except TypeError:
            pass

        table_data = list(self.current_sale_items)
        self.sale_table.setRowCount(len(table_data))
        
        COL_ACTION = 0 # ❌ Button
        COL_PROD_NAME = 1
        COL_BATCH_NO = 2
        COL_EXPIRY = 3
        COL_QTY = 4
        COL_UNIT_PRICE = 5
        COL_UNIT_TYPE = 6
        COL_SUBTOTAL = 7
        
        self.sale_table.setColumnCount(8) # INCREASED COLUMN COUNT
        self.sale_table.setHorizontalHeaderLabels(["Remove", "Product Name", "Batch No.", "Expiry (M/Y)", "Qty (Units)", "Unit Price", "Unit Type", "Subtotal"])
        self.sale_table.horizontalHeader().setSectionResizeMode(COL_PROD_NAME, QHeaderView.ResizeMode.Stretch)
        self.sale_table.horizontalHeader().setSectionResizeMode(COL_ACTION, QHeaderView.ResizeMode.ResizeToContents) 
        self.sale_table.horizontalHeader().setSectionResizeMode(COL_QTY, QHeaderView.ResizeMode.ResizeToContents)
        
        for row_num, item in enumerate(table_data):
            
            query_batch_info = "SELECT batch_number, expiry_date FROM stock_batches WHERE batch_id = ?"
            self.db.cursor.execute(query_batch_info, (item['batch_id'],))
            batch_info = self.db.cursor.fetchone()
            
            batch_number = batch_info[0] if batch_info else "N/A"
            expiry_date = batch_info[1] if batch_info else "N/A"
            
            final_subtotal = item['qty_base_units'] * item['price_per_base_unit']
            
            # 1. CREATE REMOVE BUTTON (❌)
            remove_btn = QPushButton("❌")
            remove_btn.setToolTip(f"Remove item: {item['name']}")
            remove_btn.setFixedSize(24, 24)
            remove_btn.setStyleSheet("QPushButton {padding: 0; margin: 0; background-color: #C82333; color: white; border-radius: 4px; border: none;} QPushButton:hover {background-color: #A31F2A;}")
            remove_btn.clicked.connect(lambda checked, r=row_num: self._remove_item_from_sale(r))
            
            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.addWidget(remove_btn)
            cell_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            
            self.sale_table.setCellWidget(row_num, COL_ACTION, cell_widget)
            
            # 2. SET OTHER ITEMS 
            item_name = QTableWidgetItem(item['name'])
            batch_no_item = QTableWidgetItem(batch_number)
            expiry_item = QTableWidgetItem(expiry_date)
            
            item_qty = QTableWidgetItem(f"{item['qty_base_units']:.2f}")
            item_qty.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable)

            price_item = QTableWidgetItem(f"{item['price_per_base_unit']:.2f}")
            price_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable)  

            unit_type_item = QTableWidgetItem(item['unit_type'])
            subtotal_item = QTableWidgetItem(f"{final_subtotal:.2f}")
            
            # Disable editing for non-editable columns
            for q_item in [item_name, batch_no_item, expiry_item, unit_type_item, subtotal_item]:
                if q_item != item_qty and q_item != price_item:
                    q_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            self.sale_table.setItem(row_num, COL_PROD_NAME, item_name)
            self.sale_table.setItem(row_num, COL_BATCH_NO, batch_no_item)
            self.sale_table.setItem(row_num, COL_EXPIRY, expiry_item)
            self.sale_table.setItem(row_num, COL_QTY, item_qty)
            self.sale_table.setItem(row_num, COL_UNIT_PRICE, price_item)
            self.sale_table.setItem(row_num, COL_UNIT_TYPE, unit_type_item)
            self.sale_table.setItem(row_num, COL_SUBTOTAL, subtotal_item)
            
        self.sale_table.itemChanged.connect(self.handle_item_quantity_change)
        
        self.btn_view_preview.setEnabled(len(self.current_sale_items) > 0)
        self.finalize_button.setEnabled(False)  
        self.btn_print_receipt.setEnabled(self.last_sale_data is not None)
        
        self.update_totals()

    def update_totals(self):
        total_subtotal = sum(item['qty_base_units'] * item['price_per_base_unit'] for item in self.current_sale_items)
        
        try:
            global_discount = float(self.global_discount_input.text() or 0.0)
        except ValueError:
            global_discount = 0.0

        if global_discount > total_subtotal:
            global_discount = total_subtotal

        final_total = max(0, total_subtotal - global_discount)
        
        self.total_summary_label.setText(
            f"Subtotal: ${total_subtotal:.2f} (Before Discount)"
        )
        self.total_display.setText(f"TOTAL: ${final_total:.2f}")
        
        self._temp_totals = {
            'subtotal': total_subtotal,
            'discount': global_discount,
            'final_total': final_total
        }

    def add_item_to_sale(self):
        search_text = self.search_input.text().strip()
        
        if not search_text:
            QMessageBox.warning(self, "Input Error", "Please enter a product name.")
            self.search_input.setFocus()
            return
            
        try:
            qty_base_units_to_sell = float(self.qty_input.text() or 0.0)
            if qty_base_units_to_sell <= 0: raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", f"Quantity ({self.qty_input.placeholderText()}) must be a positive number.")
            self.qty_input.setFocus()
            self.qty_input.selectAll()
            return

        search_query = "SELECT product_id, name, units_per_pack, unit_type FROM products WHERE name = ?"
        self.db.cursor.execute(search_query, (search_text,))
        product_data = self.db.cursor.fetchone()
        
        if not product_data:
            search_param = f'%{search_text}%'
            search_query_like = "SELECT product_id, name, units_per_pack, unit_type FROM products WHERE name LIKE ? LIMIT 2"
            self.db.cursor.execute(search_query_like, (search_param,))
            results = self.db.cursor.fetchall()
            
            if len(results) != 1:
                QMessageBox.warning(self, "Error", "Product not found or ambiguous.")
                self.search_input.setFocus()
                return
            product_data = results[0]
            
        product_id, product_name, units_per_pack, unit_type = product_data  
        
        effective_units_per_pack = units_per_pack if unit_type in ['TABLET', 'CAPSULE'] and units_per_pack > 0 else 1
        
        fulfillment_chunks = self._run_fefo_fulfillment(product_id, qty_base_units_to_sell)
        if not fulfillment_chunks:
            base_unit_display = 'tabs' if unit_type == 'TABLET' else unit_type.lower()
            QMessageBox.warning(self, "Stock Error", f"Total stock insufficient for {qty_base_units_to_sell:.2f} {base_unit_display}. Check Low Stock alerts.")
            self.qty_input.setFocus()  
            return

        # Remove any existing entry for this product before adding the new, correct quantity
        self.current_sale_items = [item for item in self.current_sale_items if item['product_id'] != product_id]

        for chunk in fulfillment_chunks:
            self.current_sale_items.append({
                'product_id': product_id,
                'name': product_name,
                'batch_id': chunk['batch_id'],
                'qty_base_units': chunk['qty_base_units'],
                'price_per_base_unit': chunk['base_unit_selling_price'],  
                'cost_per_base_unit': chunk['base_unit_cost_price'],  
                'units_per_pack': effective_units_per_pack,
                'unit_type': unit_type
            })
            
        self.update_sale_table()
        
        parent_window = self.window()
        if isinstance(parent_window, QMainWindow) and hasattr(parent_window, 'statusBar'):
            parent_window.statusBar.showMessage(f"✅ Added: {product_name} x{qty_base_units_to_sell:.2f} units. Ready for next item.", 2000)

        self.search_input.clear()
        self.qty_input.setText("1")  
        self.update_quantity_label()  
        self.search_input.setFocus()  

        self.finalize_button.setEnabled(False)  
        self.btn_print_receipt.setEnabled(self.last_sale_data is not None)

    # --- MODIFIED: View sale preview and cache data for print button (UNCHANGED) ---
    def view_sale_preview(self):
        self.update_totals()
        
        if not self.current_sale_items:
            QMessageBox.warning(self, "Preview Error", "The transaction is empty. Add items first.")
            return

        if self._temp_totals['final_total'] < 0:
              QMessageBox.critical(self, "Discount Error", "Global discount applied exceeds the sale subtotal.")
              self.finalize_button.setEnabled(False)
              return
            
        # Create data structure for preview/printing
        preview_data = {
            'sale_id': 'PREVIEW',
            'subtotal': self._temp_totals['subtotal'],
            'discount': self._temp_totals['discount'],
            'final_total': self._temp_totals['final_total'],
            'payment_method': self.payment_combo.currentText(),
            'items': self.current_sale_items,
            'patient_name': self.patient_name_input.text().strip(),
            'patient_address': self.patient_address_input.text().strip(),
            'doctor_ref': self.doctor_name_input.text().strip(),
            'transaction_date': datetime.date.today().strftime('%Y-%m-%d') # Use TODAY'S DATE for preview
        }
        
        self._update_receipt_preview(preview_data)
        self.finalize_button.setEnabled(True)
        
        self.last_sale_data = preview_data
        self.btn_print_receipt.setEnabled(True)


    # --- MODIFIED: Finalize Sale (UNCHANGED) ---
    def finalize_sale(self):
        self.view_sale_preview()
        
        if not self.finalize_button.isEnabled() or self._temp_totals['final_total'] < 0:
            QMessageBox.warning(self, "Sale Error", "Please ensure the sale preview is calculated and valid before finalizing.")
            return

        total_subtotal = self._temp_totals['subtotal']
        global_discount = self._temp_totals['discount']
        final_total = self._temp_totals['final_total']
        payment_method = self.payment_combo.currentText()
        
        patient_name = self.patient_name_input.text().strip()
        patient_address = self.patient_address_input.text().strip()
        doctor_ref = self.doctor_name_input.text().strip()
        
        discount_ratio = global_discount / total_subtotal if total_subtotal > 0 else 0.0

        if doctor_ref and doctor_ref != self.DR_NAME:
            self.db.add_doctor_name(doctor_ref)
            doctor_names = self.db.get_doctor_names()
            self.doctor_completer_model.setStringList(doctor_names)
        
        try:
            with self.db.conn:  
                # 1. INSERT into Sales table
                transaction_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.db.cursor.execute(
                    "INSERT INTO sales (transaction_date, total_amount, discount, payment_method, user_id, doctor_ref, patient_name, patient_address) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (transaction_datetime, final_total, global_discount, payment_method, self.user_id, doctor_ref, patient_name, patient_address)
                )
                sale_id = self.db.cursor.lastrowid
                invoice_number = sale_id
                
                batches_to_check = set()
                sold_items_copy = list(self.current_sale_items)  
                
                # 2. INSERT into Sale_Items and UPDATE Stock Batches
                for chunk in sold_items_copy:
                    
                    chunk_base_qty = chunk['qty_base_units']
                    chunk_value = chunk_base_qty * chunk['price_per_base_unit']
                    
                    # Calculate discounted unit price and total cost price at sale
                    chunk_discount_amount = chunk_value * discount_ratio
                    net_unit_price = (chunk_value - chunk_discount_amount) / chunk_base_qty
                    cost_per_base_unit = chunk['cost_per_base_unit']  
                    
                    packs_to_deduct = chunk_base_qty / chunk['units_per_pack']
                    batches_to_check.add(chunk['batch_id'])

                    self.db.cursor.execute(
                        "INSERT INTO sale_items (sale_id, product_id, batch_id, quantity_sold, unit_price, cost_price_at_sale) VALUES (?, ?, ?, ?, ?, ?)",
                        (sale_id, chunk['product_id'], chunk['batch_id'], chunk_base_qty, net_unit_price, cost_per_base_unit)
                    )
                    
                    self.db.cursor.execute(
                        "UPDATE stock_batches SET stock_quantity = ROUND(stock_quantity - ?, 3) WHERE batch_id = ?",
                        (packs_to_deduct, chunk['batch_id'])
                    )
                
                
                # 3. Check for depleted batches and DELETE them
                for batch_id in batches_to_check:
                    self.db.cursor.execute("SELECT stock_quantity FROM stock_batches WHERE batch_id = ?", (batch_id,))
                    current_stock = self.db.cursor.fetchone()
                    
                    if current_stock and current_stock[0] < 0.001:  
                        self.db.cursor.execute("SELECT COUNT(*) FROM sale_items WHERE batch_id = ?", (batch_id,))
                        has_sales = self.db.cursor.fetchone()[0] > 0
                        self.db.cursor.execute("SELECT COUNT(*) FROM returns WHERE batch_id = ?", (batch_id,))
                        has_returns = self.db.cursor.fetchone()[0] > 0
                        
                        if not has_sales and not has_returns:
                            self.db.cursor.execute("DELETE FROM stock_batches WHERE batch_id = ?", (batch_id,))
                        else:
                            print(f"Batch {batch_id} depleted (stock zeroed) and kept for audit.")
                
                
                # --- 4. Success and state reset & LOGGING ---
                
                user_info = self.db.cursor.execute("SELECT username FROM users WHERE id=?", (self.user_id,)).fetchone()
                username = user_info[0] if user_info else 'System'
                self.db.log_action(
                    self.user_id,
                    username,
                    'SALE_FINALIZE',
                    sale_id,
                    f"Total: ${final_total:.2f}, Discount: ${global_discount:.2f}, Items: {len(sold_items_copy)}, Patient: {patient_name}"
                )

                QMessageBox.information(self, "Sale Finalized", f"Invoice #{invoice_number} finalized.\nAmount: ${final_total:.2f}")
                
                self.last_sale_data = {
                    'sale_id': invoice_number,  
                    'subtotal': total_subtotal,  
                    'discount': global_discount,  
                    'final_total': final_total,  
                    'payment_method': payment_method,  
                    'items': sold_items_copy,
                    'patient_name': patient_name,
                    'patient_address': patient_address,
                    'doctor_ref': doctor_ref,
                    'transaction_date': transaction_datetime.split(' ')[0] 
                }
                
                self.finalize_button.setEnabled(False)
                self.btn_print_receipt.setEnabled(True)
                self._update_receipt_preview(self.last_sale_data)

                # --- AUTOMATIC PRINT TRIGGER ---
                pdf_data = self._get_pdf_data(self.last_sale_data)
                self.print_receipt_action(pdf_data, is_final_sale=True, trigger_print=True)
                # -------------------------------
                
                if isinstance(self.parent().parent(), QMainWindow):
                    self.parent().parent()._check_all_alerts()
                    self.parent().parent().show_dashboard_screen()

                self.current_sale_items = []
                self.sale_table.setRowCount(0)
                
                self.patient_name_input.clear()
                self.patient_address_input.clear()
                self.doctor_name_input.clear()


        except Exception as e:
            QMessageBox.critical(self, "DB Error", f"Transaction failed: {e}")



    # ----------------------------------------------------------------------
    # --- PDF Generation Methods (UNCHANGED) ---
    # ----------------------------------------------------------------------
    
    def _get_item_row_details(self, item):
        """Formats a single sale item for the receipt preview/PDF row."""
        
        # 1. Get Batch Info
        query_batch_info = "SELECT batch_number, expiry_date FROM stock_batches WHERE batch_id = ?"
        self.db.cursor.execute(query_batch_info, (item['batch_id'],))
        batch_info = self.db.cursor.fetchone()
        batch_number = batch_info[0] if batch_info else "N/A"
        expiry_date = batch_info[1] if batch_info else "N/A"
        
        # 2. Get Manufacturer (Company) Info
        query_company = "SELECT company FROM products WHERE product_id = ?"
        self.db.cursor.execute(query_company, (item['product_id'],))
        company = self.db.cursor.fetchone()
        mfg = company[0] if company and company[0] else "N/A"

        # 3. Calculate Totals (Net Price is already discounted per unit if applicable)
        total_amount = round(item['qty_base_units'] * item['price_per_base_unit'], 2)
        
        # 4. Format Expiry (MM/YYYY)
        exp_display = f"{expiry_date[5:]}/{expiry_date[:4]}" if len(expiry_date) >= 7 else expiry_date

        # Return data optimized for PDF layout columns:
        # [Product, Mfg, Qty, Rate, Batch, Exp., Amt.]
        return [
            item['name'],
            mfg,
            f"{item['qty_base_units']:.1f}", # Qty
            f"{item['price_per_base_unit']:.2f}", # Rate (Net Unit Price)
            batch_number,
            exp_display,
            f"{total_amount:.2f}"
        ]
        
    def _get_pdf_data(self, sale_data):
        """Prepares consolidated data structure for the PDF generator."""
        
        if sale_data['sale_id'] == 'PREVIEW' or 'items' in sale_data and sale_data['items']:
            items_data = [self._get_item_row_details(item) for item in sale_data['items']]
        else:
            query = """
            SELECT  
                p.name, p.company, si.quantity_sold, si.unit_price, b.batch_number, b.expiry_date, si.quantity_sold * si.unit_price
            FROM sale_items si
            JOIN products p ON si.product_id = p.product_id
            LEFT JOIN stock_batches b ON si.batch_id = b.batch_id
            WHERE si.sale_id = ?
            """
            self.db.cursor.execute(query, (sale_data['sale_id'],))
            db_items = self.db.cursor.fetchall()

            items_data = []
            for row in db_items:
                product_name, mfg, qty, rate, batch_number, expiry_date, total = row
                exp_display = f"{expiry_date[5:]}/{expiry_date[:4]}" if expiry_date and len(expiry_date) >= 7 else expiry_date or "N/A"
                items_data.append([
                    product_name, mfg or "N/A", f"{qty:.1f}", f"{rate:.2f}", batch_number or "N/A", exp_display, f"{total:.2f}"
                ])
                
        
        amount_in_words = number_to_words(int(sale_data['final_total']))
        print_date = sale_data.get('transaction_date', datetime.date.today().strftime('%Y-%m-%d'))
        
        return {
            'sale_id': str(sale_data['sale_id']),
            'total_amount': f"{sale_data['subtotal']:.2f}", 
            'discount': f"{sale_data['discount']:.2f}",
            'grand_total': f"{sale_data['final_total']:.2f}",
            'payment_method': sale_data['payment_method'],
            'amount_in_words': amount_in_words,
            'items': items_data,
            'patient_name': sale_data.get('patient_name', 'CASH SALES'),
            'patient_address': sale_data.get('patient_address', 'N/A'),
            'doctor_ref': sale_data.get('doctor_ref', 'N/A'),
            'print_date': print_date  
        }
        
    def _get_receipt_text(self, data):
        """Generates a plain text preview of the receipt."""
        
        header = f"{self.SHOP_NAME}\n"
        header += f"{self.SHOP_ADDRESS}\n"
        header += f"{self.SHOP_DL_NO} | {self.SHOP_PHONE}\n"
        header += "="*40 + "\n"
        
        display_date = data.get('print_date', datetime.date.today().strftime('%Y-%m-%d'))
        
        header += f"Invoice: {data['sale_id']}     | Date: {display_date}\n"  
        header += f"Patient: {data.get('patient_name', 'CASH SALES')}\n"
        header += f"Doctor: {data.get('doctor_ref', 'N/A')}\n"
        header += "="*40 + "\n"
        
        items_text = f"{'Product':<15} {'Qty':>5} {'Rate':>8} {'Total':>8}\n"
        items_text += "-"*40 + "\n"
        
        for item in data['items']:
            items_text += f"{item[0][:15]:<15} {item[2]:>5} {item[3]:>8} {item[6]:>8}\n"

        items_text += "-"*40 + "\n"
        items_text += f"{'Subtotal:':<30} {data['total_amount']:>8}\n"
        items_text += f"{'Discount:':<30} {data['discount']:>8}\n"
        items_text += f"{'GRAND TOTAL:':<30} {data['grand_total']:>8}\n"
        items_text += "="*40 + "\n"
        
        words = data['amount_in_words'].replace('\n', ' ')
        items_text += f"IN WORDS: {words}\n"
        items_text += f"Payment: {data['payment_method']}\n"
        
        return header + items_text

    def _update_receipt_preview(self, sale_data):
        """Updates the text preview window based on the sale data."""
        pdf_data = self._get_pdf_data(sale_data)
        receipt_text = self._get_receipt_text(pdf_data)
        
        if len(receipt_text) > 2000:
            receipt_text = receipt_text[:2000] + "\n... (Preview truncated for length)"
            
        self.receipt_preview_label.setText(receipt_text)

    def view_and_print_receipt(self):
        """Handler for the 'Print Last Receipt' button."""
        if not self.last_sale_data:
            QMessageBox.warning(self, "Print Error", "No sale data available to print. Add items and press 'View Sale Preview'.")
            self.btn_print_receipt.setEnabled(False)
            return
            
        pdf_data = self._get_pdf_data(self.last_sale_data)
        is_final_sale = self.last_sale_data['sale_id'] != 'PREVIEW'
        self.print_receipt_action(pdf_data, is_final_sale, trigger_print=True)

    def print_receipt_action(self, pdf_data, is_final_sale, is_reprint=False, trigger_print=False):
        """Generates the PDF file and informs the user where it is saved."""
        
        id_part = str(pdf_data['sale_id'])
        filename = _get_save_path(
            invoice_id=id_part,  
            invoice_date_str=pdf_data['print_date'],
            is_reprint=is_reprint
        )
        
        try:
            generate_2bills_pdf(pdf_data, filename)
            
            display_path = os.path.dirname(filename)
            status_msg = f"Receipt PDF successfully saved to **{display_path}**.\n"
            status_msg += "Please print this file manually for the two-copy layout."
            
            if trigger_print:
                self._print_pdf_file(filename)  
                status_msg = f"Receipt PDF saved and **FILE OPENED** for printing: **{display_path}**"
                
            QMessageBox.information(self, "PDF Generated", status_msg)

        except Exception as e:
            QMessageBox.critical(self, "PDF Generation Failed", f"Could not generate PDF. Error: {e}")
            print(f"PDF GENERATION ERROR: {e}")
            
    def _print_pdf_file(self, filename):
        """Uses the universal utility function to open the PDF."""
        try:
            _open_file_in_default_viewer(filename)
            
        except Exception as e:
            print(f"❌ Critical error during file open: {e}")
            QMessageBox.critical(self, "Print Error",  
                f"Failed to open PDF file: {e}\n\nCheck if a PDF reader is installed and configured."
            )

    # ----------------------------------------------------------------------
    # --- UI Setup Methods ---
    # ----------------------------------------------------------------------

    def _setup_transaction_panel(self):
        left_panel = QVBoxLayout()
        search_grid = QGridLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Product Name (Dynamic Match)...")
        self.search_input.setCompleter(self.completer)
        self.search_input.textChanged.connect(self.update_quantity_label)
        self.search_input.selectionChanged.connect(self.show_completer_on_empty_click)
        self.search_input.returnPressed.connect(self._handle_search_return_key)
        
        self.qty_input = QLineEdit(text="1")
        self.qty_input.setFixedWidth(100)
        self.qty_input.setPlaceholderText("Units")
        self.qty_input.setValidator(QDoubleValidator(0.00, 99999.99, 2))
        self.qty_input.returnPressed.connect(self.add_item_to_sale)
        
        self.add_button = QPushButton("Add Item")
        self.add_button.clicked.connect(self.add_item_to_sale)
        self.add_button.setStyleSheet("background-color: #008080;")

        self.qty_label = QLabel("Units:")
        self.stock_status_label = QLabel("Stock: N/A") 
        self.stock_status_label.setStyleSheet("font-weight: normal; color: #6C757D;")
        
        search_grid.addWidget(QLabel("Product:"), 0, 0)
        search_grid.addWidget(self.search_input, 0, 1)
        search_grid.addWidget(self.qty_label, 0, 2)
        search_grid.addWidget(self.qty_input, 0, 3)
        search_grid.addWidget(self.add_button, 0, 4)

        search_grid.addWidget(self.stock_status_label, 1, 1, 1, 4)  
        search_grid.setRowMinimumHeight(1, 15)
        
        left_panel.addLayout(search_grid)
        
        self.sale_table = QTableWidget()
        self.sale_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.sale_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.sale_table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        left_panel.addWidget(self.sale_table)
        
        # --- REMOVED: Dedicated Remove Button (Only using the inline ❌ and DEL key) ---

        bottom_controls_vbox = QVBoxLayout()
        self.total_summary_label = QLabel("Subtotal: $0.00 (Before Discount)")
        self.total_summary_label.setStyleSheet("font-weight: bold; padding: 5px; background-color: #E9ECEF; border-radius: 4px;")
        
        self.btn_view_preview = QPushButton("REFRESH / VIEW SALE PREVIEW (Set Print Data)")
        self.btn_view_preview.clicked.connect(self.view_sale_preview)  
        self.btn_view_preview.setStyleSheet("padding: 15px; font-size: 14pt; background-color: #495057; color: white;")
        self.btn_view_preview.setEnabled(False)  
        
        bottom_controls_vbox.addWidget(self.total_summary_label)
        bottom_controls_vbox.addWidget(self.btn_view_preview)
        
        left_panel.addLayout(bottom_controls_vbox)

        self.layout().addLayout(left_panel, 3)

    def _setup_checkout_panel(self):
        right_panel = QVBoxLayout()
        right_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        payment_group = QGroupBox("Checkout & Patient Details")
        payment_layout = QGridLayout(payment_group)
        
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["Cash", "Online Payment"])
        
        self.global_discount_input = QLineEdit("0.00")
        self.global_discount_input.setValidator(QDoubleValidator(0.00, 999999.99, 2))
        self.global_discount_input.setFixedWidth(120)
        self.global_discount_input.textChanged.connect(self.update_totals)
        
        self.patient_name_input = QLineEdit()
        self.patient_name_input.setPlaceholderText("Enter patient full name")
        
        self.patient_address_input = QLineEdit()
        self.patient_address_input.setPlaceholderText("Enter patient address")
        
        self.doctor_name_input = QLineEdit()
        self.doctor_name_input.setPlaceholderText("Doctor's Name/Registration No.")
        self.doctor_name_input.setCompleter(self.doctor_completer)
        
        payment_layout.addWidget(QLabel("Payment Method:"), 0, 0); payment_layout.addWidget(self.payment_combo, 0, 1)
        payment_layout.addWidget(QLabel("Global Discount ($):"), 1, 0); payment_layout.addWidget(self.global_discount_input, 1, 1)
        
        payment_layout.addWidget(QLabel("Patient Name:"), 2, 0); payment_layout.addWidget(self.patient_name_input, 2, 1)
        payment_layout.addWidget(QLabel("Patient Address:"), 3, 0); payment_layout.addWidget(self.patient_address_input, 3, 1)
        payment_layout.addWidget(QLabel("Doctor Ref:"), 4, 0); payment_layout.addWidget(self.doctor_name_input, 4, 1)  
        
        right_panel.addWidget(payment_group)

        self.total_display = QLabel("TOTAL: $0.00")
        self.total_display.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.total_display.setStyleSheet("padding: 15px; background-color: #E9ECEF; color: #343A40; border-radius: 6px;")
        right_panel.addWidget(self.total_display)
        
        # --- Receipt Preview ---
        self.receipt_preview_label = QLabel("PDF Preview Not Available. Press 'View Sale Preview' to update totals.")
        self.receipt_preview_label.setWordWrap(True)
        self.receipt_preview_label.setStyleSheet("padding: 10px; background-color: #fff; font-family: 'Courier New', monospace; font-size: 8pt;")
        self.receipt_preview_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.receipt_preview_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        self.receipt_scroll_area = QScrollArea()
        self.receipt_scroll_area.setWidgetResizable(True)
        self.receipt_scroll_area.setWidget(self.receipt_preview_label)
        self.receipt_scroll_area.setFrameShape(QFrame.Shape.StyledPanel)
        
        right_panel.addWidget(QLabel("Receipt Preview (Text Only):"))
        right_panel.addWidget(self.receipt_scroll_area)

        # --- Finalization Buttons ---
        final_buttons_layout = QHBoxLayout()
        
        self.finalize_button = QPushButton("FINALIZE SALE")
        self.finalize_button.setStyleSheet("padding: 10px; font-size: 12pt; background-color: #008080; color: white;")
        self.finalize_button.clicked.connect(self.finalize_sale)
        self.finalize_button.setEnabled(False)

        self.btn_print_receipt = QPushButton("Open Last Bill PDF")
        self.btn_print_receipt.setStyleSheet("padding: 10px; font-size: 12pt; background-color: #6C757D; color: white;")
        self.btn_print_receipt.clicked.connect(self.view_and_print_receipt)
        self.btn_print_receipt.setEnabled(False)  

        final_buttons_layout.addWidget(self.finalize_button)
        final_buttons_layout.addWidget(self.btn_print_receipt)

        right_panel.addLayout(final_buttons_layout)
        
        info_label = QLabel("To reprint an old invoice, use the **Re-Print Old Bills** screen.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("font-style: italic; color: #6C757D; padding: 10px 0;")
        right_panel.addWidget(info_label)
        
        self.layout().addLayout(right_panel, 1)


# ==============================================================================
# NEW: OLD BILL VIEWER WIDGET (MODIFIED FOR RELIABLE PRINTING)
# ==============================================================================

# ==============================================================================
# NEW: OLD BILL VIEWER WIDGET (MODIFIED FOR RELIABLE PRINTING)
# ==============================================================================

class OldBillViewerWidget(QWidget):
    """Allows searching for a past sale by ID, viewing details, and reprinting/voiding the bill."""
    
    # Shop Details (Needed for PDF generation functions)
    SHOP_NAME = "SHREE RAM MEDICAL"
    SHOP_ADDRESS = "Bus Stand Kamtha(BK), Tq Ardhapur, Dist Nanded, 431704"
    SHOP_DL_NO = "DL No: 20*346101 / 21*346102"
    SHOP_FSSAI = "FSSAI: 21521236000113"
    SHOP_PHONE = "Phone: 9822549178"
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        # Get user ID from MainWindow for voiding/logging
        main_window = self.window()
        self.user_id = main_window.user_id if hasattr(main_window, 'user_id') else 1 
        self.last_sale_data = None  
        self.setLayout(QVBoxLayout())
        self._setup_ui()
        self.reset_state()

    def reset_state(self):
        """Resets the state of the viewer after load or on startup."""
        self.last_sale_data = None
        self.invoice_input.clear()
        self.receipt_preview_label.setText("Enter an Invoice ID and click 'Fetch Details' to load the bill.")
        self.btn_fetch_details.setEnabled(True)
        self.btn_print_bill.setEnabled(False) 
        self.btn_void_sale.setEnabled(False) 
        self.lookup_status_label.setText("Status: Ready")
        self.invoice_input.setFocus()
        
    def _setup_ui(self):
        main_h_layout = QHBoxLayout()
        
        # Left Panel: Input and Actions
        left_panel = QVBoxLayout()
        left_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        title_label = QLabel("Invoice Management (Re-Print & Void)")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #008080; margin-bottom: 10px;")
        left_panel.addWidget(title_label)
        
        input_group = QGroupBox("Invoice Lookup & Actions")
        input_layout = QVBoxLayout(input_group)
        
        self.invoice_input = QLineEdit()
        self.invoice_input.setPlaceholderText("Enter Invoice ID (e.g., 1001)")
        self.invoice_input.setValidator(QIntValidator(1, 999999))
        self.invoice_input.returnPressed.connect(self.fetch_receipt_details)
        
        self.btn_fetch_details = QPushButton("Fetch Details & Load Preview")
        self.btn_fetch_details.clicked.connect(self.fetch_receipt_details)
        self.btn_fetch_details.setStyleSheet("background-color: #495057; color: white; padding: 10px; font-size: 11pt;")
        
        self.lookup_status_label = QLabel("Status: Ready")
        self.lookup_status_label.setStyleSheet("font-weight: bold; margin-top: 5px;")
        
        # Print Button
        self.btn_print_bill = QPushButton("Open Loaded Bill PDF")
        self.btn_print_bill.clicked.connect(self.print_loaded_receipt)
        self.btn_print_bill.setStyleSheet("background-color: #008080; color: white; padding: 15px; font-size: 12pt;")
        self.btn_print_bill.setEnabled(False) 
        
        # VOID Button (NEW)
        self.btn_void_sale = QPushButton("VOID Sale (Revert Stock & Keep Audit Trail)")
        self.btn_void_sale.clicked.connect(self.void_loaded_sale)
        self.btn_void_sale.setProperty("class", "RedButton")
        self.btn_void_sale.setEnabled(False)
        
        input_layout.addWidget(QLabel("Invoice ID:"))
        input_layout.addWidget(self.invoice_input)
        input_layout.addWidget(self.btn_fetch_details)
        input_layout.addWidget(self.lookup_status_label)
        input_layout.addWidget(QLabel("---"))
        input_layout.addWidget(self.btn_print_bill)
        input_layout.addWidget(self.btn_void_sale) 
        
        left_panel.addWidget(input_group)
        left_panel.addStretch(1)
        
        # Right Panel: Preview
        right_panel = QVBoxLayout()
        self.receipt_preview_label = QLabel("Invoice details will appear here.")
        self.receipt_preview_label.setWordWrap(True)
        self.receipt_preview_label.setStyleSheet("padding: 10px; background-color: #fff; font-family: 'Courier New', monospace; font-size: 8pt;")
        self.receipt_preview_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.receipt_preview_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        receipt_scroll_area = QScrollArea()
        receipt_scroll_area.setWidgetResizable(True)
        receipt_scroll_area.setWidget(self.receipt_preview_label)
        receipt_scroll_area.setFrameShape(QFrame.Shape.StyledPanel)
        
        right_panel.addWidget(QLabel("Invoice Details Preview:"))
        right_panel.addWidget(receipt_scroll_area)
        
        main_h_layout.addLayout(left_panel, 1)
        main_h_layout.addLayout(right_panel, 2)
        self.layout().addLayout(main_h_layout)

    # -----------------------------------------------------------
    # --- CORE METHODS (Fetch, Print, VOID) ---
    # -----------------------------------------------------------

    def fetch_receipt_details(self):
        """Fetches sale details and loads the preview."""
        
        self.btn_print_bill.setEnabled(False)  
        self.btn_void_sale.setEnabled(False)
        self.last_sale_data = None
        self.lookup_status_label.setText("Status: Fetching...")
        
        try:
            sale_id = int(self.invoice_input.text().strip())
        except ValueError:
            self.lookup_status_label.setText("Status: ❌ Invalid numeric Invoice ID.")
            QMessageBox.warning(self, "Input Error", "Please enter a valid numeric Invoice ID.")
            self.invoice_input.setFocus()
            return
            
        # 1. Fetch Sale Header Data (INCLUDING STATUS)
        query_sale = "SELECT transaction_date, total_amount, discount, payment_method, doctor_ref, patient_name, patient_address, status FROM sales WHERE id = ?"
        self.db.cursor.execute(query_sale, (sale_id,))
        sale_data_row = self.db.cursor.fetchone()
        
        if not sale_data_row:
            self.lookup_status_label.setText(f"Status: ❌ Invoice ID {sale_id} not found.")
            QMessageBox.critical(self, "Error", f"Invoice ID {sale_id} not found.")
            return

        date_time, total_amount, discount, payment_method, doctor_ref, patient_name, patient_address, status = sale_data_row
        original_date = date_time.split(' ')[0] 
        
        # 2. Handle Voided Status
        if status == 'Voided':
            self.lookup_status_label.setText(f"Status: ⛔ Invoice #{sale_id} is VOIDED (Total: $0.00).")
            QMessageBox.information(self, "Voided", f"Invoice #{sale_id} is already marked as VOIDED.")
            # Set data for preview, but disable print/void actions
            sale_data = {'sale_id': sale_id, 'subtotal': 0.0, 'discount': 0.0, 'final_total': 0.0, 
                         'payment_method': payment_method, 'patient_name': patient_name, 
                         'patient_address': patient_address, 'doctor_ref': doctor_ref, 
                         'transaction_date': original_date, 'status': status}
        else:
            # 3. Build the full data structure for an active sale
            sale_data = {
                'sale_id': sale_id, 'subtotal': total_amount + discount, 'discount': discount,
                'final_total': total_amount, 'payment_method': payment_method,
                'patient_name': patient_name, 'patient_address': patient_address,
                'doctor_ref': doctor_ref, 'transaction_date': original_date, 'status': status 
            }
            self.btn_print_bill.setEnabled(True) 
            self.btn_void_sale.setEnabled(True)
            self.lookup_status_label.setText(f"Status: ✅ Invoice #{sale_id} loaded. Ready to print or void (Current Total: ${total_amount:.2f}).")
        
        # 4. Store and Update Preview
        self.last_sale_data = sale_data
        self._update_receipt_preview(sale_data) 
        
    # --- MODIFIED: Print Loaded Receipt (Uses consistent print action) ---
    def print_loaded_receipt(self):
        """Prints the receipt using the cached data after it has been fetched."""
        if not self.last_sale_data or self.last_sale_data.get('status') == 'Voided':
            QMessageBox.warning(self, "Print Error", "Please fetch an ACTIVE invoice first.")
            return

        pdf_data = self._get_pdf_data(self.last_sale_data)
        # Calls the unified print action with trigger_print=True
        self.print_receipt_action(pdf_data, is_final_sale=True, is_reprint=True, trigger_print=True)

    def void_loaded_sale(self):
        """Voids the currently loaded sale, reverting stock and marking the record."""
        if not self.last_sale_data or self.last_sale_data.get('status') == 'Voided':
            QMessageBox.warning(self, "Void Error", "No active invoice loaded to void.")
            return

        sale_id = self.last_sale_data['sale_id']
        total_amount = self.last_sale_data['final_total']
        
        reply = QMessageBox.question(self, 'CONFIRM VOID',
            f"ARE YOU SURE you want to **VOID** Invoice #{sale_id} (Original Total: ${total_amount:.2f})?\n\n"
            "The sale record will be marked 'Voided', stock will be fully restored, and the transaction value will be set to $0.00. This is the correct, auditable way to cancel a sale.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            result = self.db.soft_void_sale_transaction(sale_id, self.user_id)
            
            if result is True:
                QMessageBox.information(self, "Success", f"Invoice #{sale_id} successfully VOIDED and stock has been REVERTED.")
                self.reset_state()
                # Refresh main window dashboard/alerts
                main_window = self.window()
                if isinstance(main_window, MainWindow):
                    main_window._check_all_alerts()
                    main_window.show_dashboard_screen()
            else:
                QMessageBox.critical(self, "Void Failed", f"Void process failed. Reason: {result}")


    # -----------------------------------------------------------
    # --- REUSED PRINT UTILITIES (Modified for consistency) ---
    # -----------------------------------------------------------
    
    # NOTE: The _get_item_row_details, _get_pdf_data, and _get_receipt_text 
    # functions are lengthy and unchanged in their core logic, so they are 
    # omitted here for brevity but assumed present in the final script.
    
    def _get_item_row_details(self, item):
        """Formats a single sale item for the receipt preview/PDF row. (REUSED)"""
        
        query_batch_info = "SELECT batch_number, expiry_date FROM stock_batches WHERE batch_id = ?"
        self.db.cursor.execute(query_batch_info, (item['batch_id'],))
        batch_info = self.db.cursor.fetchone()
        batch_number = batch_info[0] if batch_info else "N/A"
        expiry_date = batch_info[1] if batch_info else "N/A"
        
        query_company = "SELECT company FROM products WHERE product_id = ?"
        self.db.cursor.execute(query_company, (item['product_id'],))
        company = self.db.cursor.fetchone()
        mfg = company[0] if company and company[0] else "N/A"

        total_amount = round(item.get('quantity_sold', item.get('qty_base_units', 0.0)) * item.get('unit_price', item.get('price_per_base_unit', 0.0)), 2)
        exp_display = f"{expiry_date[5:]}/{expiry_date[:4]}" if len(expiry_date) >= 7 else expiry_date

        return [
            item.get('name', 'N/A'), mfg, f"{item.get('quantity_sold', item.get('qty_base_units', 0.0)):.1f}", f"{item.get('unit_price', item.get('price_per_base_unit', 0.0)):.2f}", 
            batch_number, exp_display, f"{total_amount:.2f}"
        ]

    def _get_pdf_data(self, sale_data):
        """Prepares consolidated data structure for the PDF generator."""
        
        query = """
        SELECT p.name, p.company, si.quantity_sold, si.unit_price, b.batch_number, b.expiry_date, si.quantity_sold * si.unit_price
        FROM sale_items si JOIN products p ON si.product_id = p.product_id LEFT JOIN stock_batches b ON si.batch_id = b.batch_id
        WHERE si.sale_id = ?
        """
        self.db.cursor.execute(query, (sale_data['sale_id'],))
        db_items = self.db.cursor.fetchall()

        items_data = []
        is_voided = sale_data.get('status') == 'Voided'
        
        for row in db_items:
            product_name, mfg, qty, rate, batch_number, expiry_date, total = row
            exp_display = f"{expiry_date[5:]}/{expiry_date[:4]}" if expiry_date and len(expiry_date) >= 7 else expiry_date or "N/A"
            
            line_total_display = "0.00" if is_voided else f"{total:.2f}"
            
            items_data.append([
                product_name, mfg or "N/A", f"{qty:.1f}", f"{rate:.2f}", batch_number or "N/A", exp_display, line_total_display
            ])
        
        amount_in_words = number_to_words(int(sale_data['final_total']))
        print_date = sale_data.get('transaction_date', datetime.date.today().strftime('%Y-%m-%d'))
        
        final_totals = {
            'subtotal': 0.00, 'discount': 0.00, 'final_total': 0.00
        } if is_voided else {
            'subtotal': sale_data['subtotal'], 'discount': sale_data['discount'], 'final_total': sale_data['final_total']
        }
        
        return {
            'sale_id': str(sale_data['sale_id']), 'total_amount': f"{final_totals['subtotal']:.2f}", 
            'discount': f"{final_totals['discount']:.2f}", 'grand_total': f"{final_totals['final_total']:.2f}",
            'payment_method': sale_data['payment_method'], 'amount_in_words': amount_in_words,
            'items': items_data, 'patient_name': sale_data.get('patient_name', 'CASH SALES'),
            'patient_address': sale_data.get('patient_address', 'N/A'), 'doctor_ref': sale_data.get('doctor_ref', 'N/A'),
            'print_date': print_date,
            'status': sale_data.get('status', 'Finalized') 
        }
        
    def _get_receipt_text(self, data):
        """Generates a plain text preview of the receipt. (REUSED)"""
        
        is_voided = data.get('status') == 'Voided'
        
        header = f"{self.SHOP_NAME}\n{self.SHOP_ADDRESS}\n{self.SHOP_DL_NO} | {self.SHOP_PHONE}\n"
        if is_voided:
             header += "\n*** VOIDED TRANSACTION ***\n"
        header += "="*40 + "\n"
        
        display_date = data.get('print_date', datetime.date.today().strftime('%Y-%m-%d'))
        header += f"Invoice: {data['sale_id']}     | Date: {display_date}\n"  
        header += f"Patient: {data.get('patient_name', 'CASH SALES')}\nDoctor: {data.get('doctor_ref', 'N/A')}\n" + "="*40 + "\n"
        
        items_text = f"{'Product':<15} {'Qty':>5} {'Rate':>8} {'Total':>8}\n" + "-"*40 + "\n"
        for item in data['items']:
            items_text += f"{item[0][:15]:<15} {item[2]:>5} {item[3]:>8} {item[6]:>8}\n"

        items_text += "-"*40 + "\n"
        items_text += f"{'Subtotal:':<30} {data['total_amount']:>8}\n"
        items_text += f"{'Discount:':<30} {data['discount']:>8}\n"
        items_text += f"{'GRAND TOTAL:':<30} {data['grand_total']:>8}\n" + "="*40 + "\n"
        
        words = data['amount_in_words'].replace('\n', ' ')
        items_text += f"IN WORDS: {words}\nPayment: {data['payment_method']}\n"
        
        return header + items_text

    def _update_receipt_preview(self, sale_data):
        """Updates the text preview window based on the sale data. (REUSED)"""
        pdf_data = self._get_pdf_data(sale_data)
        receipt_text = self._get_receipt_text(pdf_data)
        
        if len(receipt_text) > 2000:
            receipt_text = receipt_text[:2000] + "\n... (Preview truncated for length)"
            
        self.receipt_preview_label.setText(receipt_text)
        
    def print_receipt_action(self, pdf_data, is_final_sale, is_reprint=False, trigger_print=False):
        """Generates the PDF file and informs the user where it is saved."""
        
        id_part = str(pdf_data['sale_id'])
        
        # Use the new utility function to get the dynamic save path
        filename = _get_save_path(
            invoice_id=id_part, 
            invoice_date_str=pdf_data['print_date'],
            is_reprint=is_reprint
        )
            
        try:
            # External function call to ReportLab for dual-bill PDF
            generate_2bills_pdf(pdf_data, filename)
            
            # Extract only the base directory for display
            display_path = os.path.dirname(filename)
            
            status_msg = f"Invoice PDF successfully saved to **{display_path}**.\n"
            status_msg += "The file will be opened for printing/viewing."
            
            # --- CONSISTENT PRINT LOGIC (System Open) ---
            if trigger_print:
                # Calls the new, simplified utility function
                _print_pdf_file_consistent(filename, self)
                status_msg = f"Invoice PDF saved and **FILE OPENED** for printing: **{display_path}**"
                
            QMessageBox.information(self, "PDF Generated", status_msg)

        except Exception as e:
            QMessageBox.critical(self, "Print Failed", f"Could not generate PDF. Error: {e}")
            print(f"PDF GENERATION ERROR: {e}")         
            
# --- NOTE: The redundant _print_pdf_file is now replaced by the global _print_pdf_file_consistent ---
# --- No additional methods are needed inside the class for printing. ---

# ==============================================================================
# 3. PURCHASING WIDGETS (NEW - ORDER ENTRY & PAYMENT MANAGEMENT) - COMPLETE
# ==============================================================================

# ==============================================================================
# 3. PURCHASING WIDGETS - OrderEntryWidget (MODIFIED: Supplier Input/Selection)
# ==============================================================================

class OrderEntryWidget(QWidget):
    """Allows input of new purchase orders and receipt of stock."""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.pending_order_items = []
        self.supplier_names = self.db.get_supplier_names() # Pre-load for combo box
        self._setup_ui()
        self._setup_autocompleters()
        
    def _setup_autocompleters(self):
        # Product Completer
        product_names = self.db.get_product_names()
        self.product_completer_model = QStringListModel(product_names)
        self.product_completer = QCompleter(self.product_completer_model)
        self.product_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.product_completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.product_search_input.setCompleter(self.product_completer)
        self.product_search_input.textChanged.connect(self.load_product_info)
        
        # NOTE: Supplier Completer removed; selection is now via QComboBox

    # --- NEW: Function to sync supplier selection from combo to read-only input ---
    def _sync_supplier_selection(self, index):
        selected_supplier = self.supplier_combo.currentText()
        if selected_supplier == "--- Select Existing Supplier ---":
            self.supplier_input.clear()
        else:
            self.supplier_input.setText(selected_supplier)

    def load_product_info(self):
        """Loads static product info (units/pack, unit_type) but requires manual price entry."""
        product_name = self.product_search_input.text().strip()
        self.current_product_data = None
        
        if not product_name:
            self.product_status_label.setText("Status: Ready to search product.")
            self.add_item_button.setEnabled(False)
            self.pack_cost_input.clear()
            self.pack_selling_input.clear()
            return

        # Query only for static info
        query = "SELECT product_id, units_per_pack, unit_type FROM products WHERE name = ?"
        self.db.cursor.execute(query, (product_name,))
        result = self.db.cursor.fetchone()
        
        if result:
            product_id, units_per_pack, unit_type = result
            self.current_product_data = {'id': product_id, 'units_per_pack': units_per_pack, 'unit_type': unit_type}
            
            self.pack_cost_input.clear()
            self.pack_selling_input.clear()
            self.product_status_label.setText(f"Status: Units/Pack: {units_per_pack}. **Enter current Cost and Selling Price from invoice.**")
            self.add_item_button.setEnabled(True)
        else:
            self.product_status_label.setText("Status: Product NOT FOUND.")
            self.pack_cost_input.clear()
            self.pack_selling_input.clear()
            self.add_item_button.setEnabled(False)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)

        def create_dense_label(text):
            label = QLabel(text)
            label.setStyleSheet("font-size: 9pt; min-height: 18px;")
            return label

        line_edit_style = "QLineEdit, QDateEdit, QComboBox {padding: 5px 8px; min-height: 20px; font-size: 9pt;}"
        
        # 1. Header and Supplier Info 
        header_group = QGroupBox("Invoice/Supplier Details")
        header_group.setStyleSheet("QGroupBox {padding: 5px; margin-top: 5px; font-size: 10pt;}")
        header_layout = QGridLayout(header_group)
        header_layout.setContentsMargins(5, 15, 5, 5)
        header_layout.setVerticalSpacing(5)
        
        # --- MODIFIED: Supplier Input/Selection ---
        # 1. Read-only input to hold the final selection
        self.supplier_input = QLineEdit()
        self.supplier_input.setStyleSheet("background-color: #E9ECEF; color: #343A40;") # Gray background for read-only
        self.supplier_input.setReadOnly(True)
        self.supplier_input.setPlaceholderText("Select supplier below...")
        
        # 2. ComboBox for selecting existing suppliers
        self.supplier_combo = QComboBox()
        self.supplier_combo.addItems(["--- Select Existing Supplier ---"] + sorted(self.supplier_names))
        self.supplier_combo.setStyleSheet(line_edit_style)
        self.supplier_combo.currentIndexChanged.connect(self._sync_supplier_selection)

        self.invoice_number_input = QLineEdit(); self.invoice_number_input.setStyleSheet(line_edit_style)
        self.invoice_date_input = QDateEdit(QDate.currentDate()); self.invoice_date_input.setCalendarPopup(True)
        self.invoice_date_input.setDisplayFormat("yyyy-MM-dd"); self.invoice_date_input.setStyleSheet(line_edit_style)
        
        # Display the read-only input and the selection combo
        header_layout.addWidget(create_dense_label("Selected Supplier:"), 0, 0); header_layout.addWidget(self.supplier_input, 0, 1)
        header_layout.addWidget(create_dense_label("Select Supplier:"), 1, 0); header_layout.addWidget(self.supplier_combo, 1, 1)
        
        header_layout.addWidget(create_dense_label("Invoice No:"), 2, 0); header_layout.addWidget(self.invoice_number_input, 2, 1)
        header_layout.addWidget(create_dense_label("Invoice Date:"), 3, 0); header_layout.addWidget(self.invoice_date_input, 3, 1)
        
        main_layout.addWidget(header_group)
        
        # 2. Add Item Section 
        item_group = QGroupBox("Add/Receive Items")
        item_group.setStyleSheet("QGroupBox {padding: 5px; margin-top: 5px; font-size: 10pt;}")
        item_layout = QGridLayout(item_group)
        item_layout.setContentsMargins(5, 15, 5, 5)
        item_layout.setVerticalSpacing(5)
        
        self.product_search_input = QLineEdit()
        self.qty_input = QLineEdit("1.0"); self.qty_input.setValidator(QDoubleValidator(0.00, 99999.99, 2))
        self.pack_cost_input = QLineEdit(); self.pack_cost_input.setValidator(QDoubleValidator(0.00, 99999.99, 2))
        self.pack_selling_input = QLineEdit() 
        self.pack_selling_input.setValidator(QDoubleValidator(0.00, 99999.99, 2)) 
        self.batch_number_input = QLineEdit()
        self.expiry_input = QDateEdit(QDate.currentDate().addYears(1)); self.expiry_input.setCalendarPopup(True)
        self.expiry_input.setDisplayFormat("yyyy-MM")
        
        self.product_search_input.setStyleSheet(line_edit_style)
        self.qty_input.setStyleSheet(line_edit_style)
        self.pack_cost_input.setStyleSheet(line_edit_style)
        self.pack_selling_input.setStyleSheet(line_edit_style) 
        self.batch_number_input.setStyleSheet(line_edit_style)
        self.expiry_input.setStyleSheet(line_edit_style)
        
        self.add_item_button = QPushButton("Add Item to Receipt List")
        self.add_item_button.clicked.connect(self.add_item_to_list)
        self.add_item_button.setStyleSheet("background-color: #008080; color: white; padding: 8px;")
        self.add_item_button.setEnabled(False)
        
        self.product_status_label = QLabel("Status: Ready to search product.")
        self.product_status_label.setStyleSheet("font-weight: bold; color: #6C757D; font-size: 9pt;")

        item_layout.addWidget(create_dense_label("Product:"), 0, 0); item_layout.addWidget(self.product_search_input, 0, 1)
        item_layout.addWidget(create_dense_label("Qty (Packs):"), 1, 0); item_layout.addWidget(self.qty_input, 1, 1)
        item_layout.addWidget(create_dense_label("Pack Cost ($):"), 2, 0); item_layout.addWidget(self.pack_cost_input, 2, 1)
        item_layout.addWidget(create_dense_label("Pack Selling ($):"), 3, 0); item_layout.addWidget(self.pack_selling_input, 3, 1) 

        item_layout.addWidget(create_dense_label("Batch No:"), 0, 2); item_layout.addWidget(self.batch_number_input, 0, 3)
        item_layout.addWidget(create_dense_label("Expiry (M/Y):"), 1, 2); item_layout.addWidget(self.expiry_input, 1, 3)
        item_layout.addWidget(self.add_item_button, 4, 2, 1, 2) 
        item_layout.addWidget(self.product_status_label, 5, 0, 1, 4) 
        
        main_layout.addWidget(item_group)
        
        # 3. Pending List and Finalize (UNCHANGED)
        pending_group = QGroupBox("Receipt/Order Items")
        pending_layout = QVBoxLayout(pending_group)
        
        self.pending_table = QTableWidget()
        self.pending_table.setColumnCount(6)
        self.pending_table.setHorizontalHeaderLabels(["Product", "Batch No.", "Qty (Packs)", "Cost/Pack ($)", "Total ($)", "Expiry (M/Y)"])
        self.pending_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        pending_layout.addWidget(self.pending_table)
        
        self.total_order_amount_label = QLabel("TOTAL INVOICE AMOUNT: $0.00")
        self.total_order_amount_label.setStyleSheet("font-size: 14pt; font-weight: bold; padding: 5px; background-color: #E9ECEF;")
        
        finalize_hlayout = QHBoxLayout()
        self.remove_item_button = QPushButton("Remove Selected Item")
        self.remove_item_button.setProperty("class", "RedButton")
        self.remove_item_button.clicked.connect(self.remove_item_from_list)
        self.finalize_order_button = QPushButton("FINALIZE ORDER & RECEIVE STOCK")
        self.finalize_order_button.setStyleSheet("padding: 15px; font-size: 16pt; background-color: #495057; color: white;")
        self.finalize_order_button.clicked.connect(self.finalize_order)
        self.finalize_order_button.setEnabled(False)

        finalize_hlayout.addWidget(self.remove_item_button)
        finalize_hlayout.addWidget(self.total_order_amount_label)
        finalize_hlayout.addWidget(self.finalize_order_button)
        pending_layout.addLayout(finalize_hlayout)
        
        main_layout.addWidget(pending_group)

    def add_item_to_list(self):
        # 1. Product Name Validation
        if not self.current_product_data:
            QMessageBox.warning(self, "Product Error", "Please select a valid product from the list.")
            self.product_search_input.setFocus()
            return
            
        supplier_name = self.supplier_input.text().strip() # Get supplier from read-only field
        batch_number = self.batch_number_input.text().strip()
        
        # 2. Numeric Input Validation 
        try:
            qty = float(self.qty_input.text())
            cost = float(self.pack_cost_input.text())
            selling = float(self.pack_selling_input.text()) 
            if qty <= 0 or cost <= 0 or selling <= 0: raise ValueError 
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Quantity, Cost, and Selling Price must be positive numbers.")
            self.qty_input.setFocus()
            self.qty_input.selectAll()
            return

        # 3. Required Field Check 
        if not supplier_name: # Check the read-only field
            QMessageBox.warning(self, "Input Error", "Please select a Supplier Name from the dropdown above.")
            self.supplier_combo.setFocus()
            return
            
        if not batch_number:
            QMessageBox.warning(self, "Input Error", "Batch Number is required.")
            self.batch_number_input.setFocus()
            return

        product_id = self.current_product_data['id']
        product_name = self.product_search_input.text().strip()
        expiry_date = self.expiry_input.date().toString("yyyy-MM")
        
        self.pending_order_items.append({
            'product_id': product_id,
            'product_name': product_name,
            'batch_number': batch_number,
            'pack_quantity': qty,
            'pack_cost': cost,
            'pack_selling_price': selling, 
            'expiry_date': expiry_date
        })
        
        self.update_pending_table()
        
        main_window = self.window()
        if isinstance(main_window, QMainWindow) and hasattr(main_window, 'statusBar'):
            main_window.statusBar.showMessage(f"✅ Item added: {product_name} x {qty:.2f} packs.", 2000)

        # Reset item inputs for fast entry
        self.product_search_input.clear()
        self.batch_number_input.clear()
        self.qty_input.setText("1.0")
        self.pack_cost_input.clear()
        self.pack_selling_input.clear() 
        self.product_search_input.setFocus()

    def remove_item_from_list(self):
        selected_rows = self.pending_table.selectedItems()
        if not selected_rows: return
        
        row_index = selected_rows[0].row()
        item_name = self.pending_table.item(row_index, 0).text()
        self.pending_order_items.pop(row_index)
        self.update_pending_table()
        
        main_window = self.window()
        if isinstance(main_window, QMainWindow) and hasattr(main_window, 'statusBar'):
             main_window.statusBar.showMessage(f"🗑️ Removed item: {item_name}.", 2000)

    def update_pending_table(self):
        self.pending_table.setRowCount(len(self.pending_order_items))
        total_amount = 0.0
        
        for row_num, item in enumerate(self.pending_order_items):
            line_total = item['pack_quantity'] * item['pack_cost']
            total_amount += line_total
            
            data = [
                item['product_name'], item['batch_number'], f"{item['pack_quantity']:.2f}",
                f"{item['pack_cost']:.2f}", f"{line_total:.2f}", item['expiry_date']
            ]
            
            for col, value in enumerate(data):
                self.pending_table.setItem(row_num, col, QTableWidgetItem(value))
                
        self.total_order_amount_label.setText(f"TOTAL INVOICE AMOUNT: ${total_amount:.2f}")
        self.finalize_order_button.setEnabled(len(self.pending_order_items) > 0)
        self.pending_table.resizeColumnsToContents()
        
    def finalize_order(self):
        if not self.pending_order_items: return
        
        supplier_name = self.supplier_input.text().strip()
        invoice_number = self.invoice_number_input.text().strip()
        invoice_date = self.invoice_date_input.date().toString("yyyy-MM-dd")
        total_amount = sum(item['pack_quantity'] * item['pack_cost'] for item in self.pending_order_items)

        if not supplier_name:
            QMessageBox.warning(self, "Error", "Supplier Name is required. Select one from the list.")
            self.supplier_combo.setFocus()
            return

        reply = QMessageBox.question(self, 'Confirm Receipt',
            f"Confirm receipt of {len(self.pending_order_items)} items from **{supplier_name}** for a total of **${total_amount:.2f}**? \n\nStock will be added and a Payable Invoice created.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # Note: We rely on the Supplier Management tab to add the supplier name.
            # No need to call self.db.add_supplier_name(supplier_name) here, but it's safe if it exists.
            
            # 1. Create the purchase order and receive stock
            order_id = self.db.create_purchase_order(supplier_name, self.pending_order_items)
            
            if order_id:
                # 2. Update the invoice details on the newly created order
                try:
                    with self.db.conn:
                        self.db.cursor.execute(
                            "UPDATE purchase_orders SET invoice_number = ?, invoice_date = ? WHERE order_id = ?",
                            (invoice_number, invoice_date, order_id)
                        )
                except Exception as e:
                     QMessageBox.warning(self, "DB Update Warning", f"Order created but failed to update invoice details: {e}")

                # NEW: Log the Order Receipt event (user retrieval unchanged)
                main_window = self.window()
                user_info = self.db.cursor.execute("SELECT username FROM users WHERE id=?", (main_window.user_id,)).fetchone()
                username = user_info[0] if user_info else 'System'
                self.db.log_action(
                    main_window.user_id,
                    username,
                    'ORDER_RECEIVE',
                    order_id,
                    f"Supplier: {supplier_name}, Inv No: {invoice_number}, Total: ${total_amount:.2f}"
                )

                QMessageBox.information(self, "Success", f"Order #{order_id} (Invoice: {invoice_number}) received and stock added. Total Payable: ${total_amount:.2f}.")
                
                # Reset UI
                self.pending_order_items = []
                self.update_pending_table()
                # Clear all supplier selection fields
                self.supplier_input.clear()
                self.supplier_combo.setCurrentIndex(0) 
                self.invoice_number_input.clear()
                self.invoice_date_input.setDate(QDate.currentDate())
                self.product_search_input.setFocus()
            else:
                QMessageBox.critical(self, "DB Error", "Failed to finalize order and receive stock.")


# In PurchasingWidget class, replace SupplierPaymentsWidget with this:

class POManagerWidget(QWidget):
    """Manages viewing, voiding, and recording payments for all Purchase Orders."""
    
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self._setup_ui()
        self.load_pending_invoices() # Still loads pending by default

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Helper function for dense labels
        def create_dense_label(text):
            label = QLabel(text)
            label.setStyleSheet("font-size: 9pt; min-height: 18px; margin-top: 5px;")
            return label

        # Apply reduced height/padding to inputs
        line_edit_style = "QLineEdit, QDateEdit, QComboBox {padding: 5px 8px; min-height: 20px; font-size: 9pt;}"
        
        # 1. Purchase Orders List (Payables)
        payables_group = QGroupBox("1. Purchase Orders List")
        # Apply reduced margins to gain space
        payables_group.setStyleSheet("QGroupBox {padding: 5px; margin-top: 5px; font-size: 10pt;}")
        payables_layout = QVBoxLayout(payables_group)
        payables_layout.setContentsMargins(5, 15, 5, 5) 
        
        # Search & Toggle Layout (Horizontal)
        search_toggle_hlayout = QHBoxLayout()
        
        self.search_po_input = QLineEdit()
        self.search_po_input.setPlaceholderText("Filter by Order ID, Supplier Name, or Invoice No...")
        self.search_po_input.textChanged.connect(self.load_pending_invoices)
        self.search_po_input.setStyleSheet(line_edit_style)

        self.btn_toggle_po_view = QPushButton("Toggle: PENDING/UNPAID Orders")
        self.btn_toggle_po_view.setProperty("class", "GraySecondary")
        self.btn_toggle_po_view.clicked.connect(self._toggle_all_pos)
        self.btn_toggle_po_view.setMinimumWidth(250)
        self.btn_toggle_po_view.setStyleSheet("min-height: 36px;") # Standard button height
        
        search_toggle_hlayout.addWidget(create_dense_label("Filter:"))
        search_toggle_hlayout.addWidget(self.search_po_input)
        search_toggle_hlayout.addWidget(self.btn_toggle_po_view)
        payables_layout.addLayout(search_toggle_hlayout)

        self.payables_table = QTableWidget()
        self.payables_table.setColumnCount(8)
        self.payables_table.setHorizontalHeaderLabels(["Order ID", "Status", "Supplier", "Invoice No", "Total Amt ($)", "Paid ($)", "Credit ($)", "Pending ($)"])
        self.payables_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.payables_table.horizontalHeader().setMinimumSectionSize(50) # Prevent sections from disappearing
        self.payables_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.payables_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.payables_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.payables_table.cellClicked.connect(self.update_payment_context)
        
        payables_layout.addWidget(self.payables_table)
        main_layout.addWidget(payables_group)

        # 2. Action Buttons (View Items / Void PO)
        action_hlayout = QHBoxLayout()
        self.btn_view_po_items = QPushButton("View Line Items")
        self.btn_view_po_items.clicked.connect(self.view_po_details)
        self.btn_view_po_items.setProperty("class", "BlueButton")
        self.btn_view_po_items.setEnabled(False)
        self.btn_view_po_items.setStyleSheet("min-height: 36px;")
        
        self.btn_void_po = QPushButton("VOID Purchase Order (Irreversible)")
        self.btn_void_po.clicked.connect(self.void_selected_po)
        self.btn_void_po.setProperty("class", "RedCritical")
        self.btn_void_po.setEnabled(False)
        self.btn_void_po.setStyleSheet("min-height: 36px;")
        
        action_hlayout.addWidget(self.btn_view_po_items)
        action_hlayout.addWidget(self.btn_void_po)
        main_layout.addLayout(action_hlayout)
        
        # 3. Payment Entry (Reduced Density Group Box)
        payment_group = QGroupBox("2. Record Payment")
        payment_group.setStyleSheet("QGroupBox {padding: 5px; margin-top: 5px; font-size: 10pt;}")
        payment_layout = QGridLayout(payment_group)
        payment_layout.setContentsMargins(5, 15, 5, 5) 
        payment_layout.setVerticalSpacing(5)
        
        self.current_order_id = QLabel("N/A")
        self.current_supplier = QLabel("N/A")
        self.current_pending_amount = QLabel("$0.00")
        
        self.payment_amount_input = QLineEdit("0.00")
        self.payment_amount_input.setValidator(QDoubleValidator(0.00, 9999999.99, 2))
        self.payment_amount_input.setStyleSheet(line_edit_style)
        
        self.payment_method_combo = QComboBox()
        self.payment_method_combo.addItems(["Cash", "Bank Transfer", "Cheque", "UPI"])
        self.payment_method_combo.setStyleSheet(line_edit_style)
        
        self.transaction_ref_input = QLineEdit()
        self.transaction_ref_input.setPlaceholderText("Bill/Cheque/UPI ID/Reference Number")
        self.transaction_ref_input.setStyleSheet(line_edit_style)
        
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Payment details or notes")
        self.notes_input.setStyleSheet(line_edit_style)
        
        self.process_payment_button = QPushButton("Process Payment")
        self.process_payment_button.clicked.connect(self.process_payment)
        self.process_payment_button.setStyleSheet("background-color: #008080; color: white; padding: 8px;") # Smaller padding
        self.process_payment_button.setEnabled(False)

        # Row 0-2: Context
        payment_layout.addWidget(create_dense_label("Selected Order ID:"), 0, 0); payment_layout.addWidget(self.current_order_id, 0, 1)
        payment_layout.addWidget(create_dense_label("Supplier:"), 1, 0); payment_layout.addWidget(self.current_supplier, 1, 1)
        payment_layout.addWidget(create_dense_label("Pending Amount:"), 2, 0); payment_layout.addWidget(self.current_pending_amount, 2, 1)
        
        # Row 3-6: Inputs
        payment_layout.addWidget(create_dense_label("Payment Method:"), 3, 0); payment_layout.addWidget(self.payment_method_combo, 3, 1)
        payment_layout.addWidget(create_dense_label("Amount to Pay ($):"), 4, 0); payment_layout.addWidget(self.payment_amount_input, 4, 1)
        payment_layout.addWidget(create_dense_label("Reference ID:"), 5, 0); payment_layout.addWidget(self.transaction_ref_input, 5, 1)
        payment_layout.addWidget(create_dense_label("Notes:"), 6, 0); payment_layout.addWidget(self.notes_input, 6, 1)

        payment_layout.addWidget(self.process_payment_button, 7, 0, 1, 2)
        
        main_layout.addWidget(payment_group)
        main_layout.addStretch(1)

    def _toggle_all_pos(self):
        """Toggles between showing only pending and showing all POs."""
        if self.btn_toggle_po_view.text().startswith("Toggle: Currently Showing PENDING"):
            self.btn_toggle_po_view.setText("Toggle: Currently Showing ALL ORDERS (Including Paid/Voided)")
        else:
            self.btn_toggle_po_view.setText("Toggle: Currently Showing PENDING/UNPAID Orders")
        self.load_pending_invoices() # Reloads based on the new button text

    def load_pending_invoices(self):
        """Modified to load all or only pending invoices based on toggle state and filter."""
        show_all = self.btn_toggle_po_view.text().startswith("Toggle: Currently Showing ALL")
        search_text = self.search_po_input.text().strip().lower()
        
        if show_all:
            # Query to get ALL orders
            query = """
            SELECT order_id, supplier_name, total_invoice_amount, status, invoice_number, invoice_date
            FROM purchase_orders
            ORDER BY order_id DESC;
            """
            self.db.cursor.execute(query)
            raw_orders = self.db.cursor.fetchall()
            
            invoices = []
            for order_id, supplier_name, total_invoice, status, inv_num, inv_date in raw_orders:
                # Calculate live paid/credit/pending for ALL orders
                self.db.cursor.execute("SELECT COALESCE(SUM(amount_paid), 0.0) FROM supplier_payments WHERE order_id = ?", (order_id,))
                total_paid = self.db.cursor.fetchone()[0] or 0.0
                return_credit = self.db.get_order_returns_credit(order_id)
                net_pending = total_invoice - total_paid - return_credit
                
                # Filter by search text if provided
                if search_text and not any(search_text in str(x).lower() for x in (order_id, supplier_name, inv_num, status)):
                    continue
                    
                invoices.append({
                    'order_id': order_id,
                    'supplier_name': supplier_name,
                    'invoice_number': inv_num or 'N/A',
                    'total_invoice_amount': total_invoice,
                    'total_paid': total_paid,
                    'return_credit': return_credit,
                    'net_pending': net_pending,
                    'status': status
                })
        else:
            # Original logic for PENDING only (handles its own filtering for 'Voided')
            invoices = self.db.get_supplier_pending_invoices()
            invoices = [inv for inv in invoices if not search_text or any(search_text in str(x).lower() for x in (inv['order_id'], inv['supplier_name'], inv['invoice_number']))]

        self.payables_table.setRowCount(len(invoices))
        self.btn_view_po_items.setEnabled(False)
        self.btn_void_po.setEnabled(False)

        for row_num, inv in enumerate(invoices):
            data = [
                str(inv['order_id']), inv.get('status', 'Unpaid'), inv['supplier_name'], inv['invoice_number'],
                f"{inv['total_invoice_amount']:.2f}", f"{inv['total_paid']:.2f}",
                f"{inv['return_credit']:.2f}", f"{inv['net_pending']:.2f}"
            ]
            
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter if col in [0, 4, 5, 6, 7] else Qt.AlignmentFlag.AlignLeft)
                
                # Color coding based on status
                if inv.get('status') == 'Paid':
                    item.setBackground(QColor(200, 255, 200)) # Green
                elif inv.get('status') == 'Voided':
                    item.setBackground(QColor(255, 200, 200)) # Red
                elif inv.get('status') == 'Received/Unpaid' and inv['net_pending'] > 0.001:
                    item.setBackground(QColor(255, 255, 200)) # Yellow
                
                self.payables_table.setItem(row_num, col, item)
                
        self.payables_table.resizeColumnsToContents()
        self.current_order_id.setText("N/A")
        self.current_supplier.setText("N/A")
        self.current_pending_amount.setText("$0.00")
        self.payment_amount_input.setText("0.00") # Clear input too

    def update_payment_context(self):
        """Updates the payment form context AND enables View/Void buttons."""
        selected_items = self.payables_table.selectedItems()
        if not selected_items:
            self.process_payment_button.setEnabled(False)
            self.btn_view_po_items.setEnabled(False)
            self.btn_void_po.setEnabled(False)
            return

        row_index = selected_items[0].row()
        order_id = int(self.payables_table.item(row_index, 0).text())
        status = self.payables_table.item(row_index, 1).text()
        supplier_name = self.payables_table.item(row_index, 2).text()
        pending_text = self.payables_table.item(row_index, 7).text().replace('$', '')
        pending_amount = float(pending_text)

        self.current_order_id.setText(str(order_id))
        self.current_supplier.setText(supplier_name)
        self.current_pending_amount.setText(f"${pending_amount:.2f}")
        self.payment_amount_input.setText(f"{pending_amount:.2f}")

        # Enable buttons based on status and pending amount
        self.btn_view_po_items.setEnabled(True)
        self.process_payment_button.setEnabled(pending_amount > 0.001)
        
        # Only allow voiding if the status is not already Paid/Voided AND there are pending funds
        self.btn_void_po.setEnabled(status == 'Received/Unpaid' and pending_amount > 0.001)
        if status == 'Paid' or status == 'Voided':
             self.btn_void_po.setEnabled(False) 

    def view_po_details(self):
        """Opens a dialog to show line items of the selected PO."""
        try:
            order_id = int(self.current_order_id.text())
            if order_id == 0: return
            dialog = PurchaseOrderDetailDialog(self.db, order_id, self)
            dialog.exec()
        except ValueError:
            QMessageBox.warning(self, "Selection Error", "Please select a valid Order ID.")
            
    def void_selected_po(self):
        """Attempts to soft void the selected Purchase Order."""
        try:
            order_id = int(self.current_order_id.text())
        except ValueError:
            QMessageBox.warning(self, "Selection Error", "Please select a Purchase Order to void.")
            return

        reply = QMessageBox.question(self, 'CONFIRM VOID PO',
            f"Are you SURE you want to **VOID** Purchase Order #{order_id}?\n\n"
            "This action will **REVERT ALL UNUSED STOCK** and **CANCEL THE PAYABLE**.\n**CANNOT BE UNDONE!**",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # Need access to MainWindow's user_id for logging
            main_window = self.window()
            user_id = main_window.user_id if hasattr(main_window, 'user_id') else 1

            result = self.db.soft_void_purchase_order(order_id, user_id)
            
            if result is True:
                QMessageBox.information(self, "Success", f"Purchase Order #{order_id} successfully VOIDED and stock reverted.")
            elif isinstance(result, str):
                QMessageBox.critical(self, "Void Failed", f"PO Void failed. Reason: {result}")
            else:
                QMessageBox.critical(self, "Void Failed", "An unknown error occurred during the database transaction.")
            
            self.load_pending_invoices()
            if isinstance(main_window, MainWindow):
                 main_window._check_all_alerts()
                 main_window.show_dashboard_screen()
            
    def process_payment(self):
        try:
            order_id = int(self.current_order_id.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "No invoice selected. Please select a row from the PO List.")
            return

        try:
            amount_to_pay = float(self.payment_amount_input.text())
            if amount_to_pay <= 0: raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid payment amount.")
            return

        payment_method = self.payment_method_combo.currentText()
        transaction_ref = self.transaction_ref_input.text().strip()
        notes = self.notes_input.text().strip()
        
        pending_amount_text = self.current_pending_amount.text().replace('$', '')
        max_pending = float(pending_amount_text)
        
        if amount_to_pay > max_pending + 0.001:
            QMessageBox.warning(self, "Payment Error", f"Payment amount (${amount_to_pay:.2f}) exceeds pending amount (${max_pending:.2f}).")
            return
            
        reply = QMessageBox.question(self, 'Confirm Payment',
            f"Confirm payment of **${amount_to_pay:.2f}** to **{self.current_supplier.text()}** (Order #{order_id}) via {payment_method}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            success = self.db.record_supplier_payment(order_id, amount_to_pay, payment_method, transaction_ref, notes, self.user_id)
            
            if success:
                QMessageBox.information(self, "Success", f"Payment of ${amount_to_pay:.2f} recorded successfully.")
                self.load_pending_invoices()
            else:
                QMessageBox.critical(self, "DB Critical Error", "Payment failed to record due to a database integrity error. Check console for details and ensure the selected Order ID is valid.")

# In PurchasingWidget class, replace the whole class with this:

# ==============================================================================
# 3. PURCHASING WIDGET (MODIFIED to include SupplierManagementWidget)
# ==============================================================================

class PurchasingWidget(QTabWidget):
    """Container for Purchase Order Entry, Supplier Payments, and Supplier Management."""
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        
        self.order_entry_widget = OrderEntryWidget(self.db)
        self.po_manager_widget = POManagerWidget(self.db, self.user_id)
        # >>> NEW: Supplier Management Tab <<<
        self.supplier_management_widget = SupplierManagementWidget(self.db, self.user_id)
        
        self.addTab(self.order_entry_widget, "1. Receive Stock & Create Invoice")
        self.addTab(self.po_manager_widget, "2. Manage Purchase Orders & Payments")
        self.addTab(self.supplier_management_widget, "3. Supplier Master & Ledger") # <<< NEW TAB
        
        self.currentChanged.connect(self._handle_tab_change)

    def _handle_tab_change(self, index):
        if self.tabText(index) == "2. Manage Purchase Orders & Payments":
            self.po_manager_widget.load_pending_invoices()
        # >>> NEW: Reload supplier list when the tab is switched to <<<
        elif self.tabText(index) == "3. Supplier Master & Ledger":
            self.supplier_management_widget.load_suppliers()     
            
# ==============================================================================
# 4. REPORTS WIDGET (ANALYTICS) - COMPLETE
# ==============================================================================

# ==============================================================================
# NEW: PO VIEWER DIALOG (for Supplier Ledger and PO Manager)
# ==============================================================================

class POViewerDialog(QDialog):
    """Read-only dialog to show the full details of a specific Purchase Order."""
    
    def __init__(self, db, order_id, parent=None):
        super().__init__(parent)
        self.db = db
        self.order_id = order_id
        self.setWindowTitle(f"Purchase Order Viewer: #{order_id}")
        self.setMinimumSize(850, 600)
        self._setup_ui()
        self.load_po_details()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # 1. Header Details (Supplier, Invoice, Status, Totals)
        header_group = QGroupBox("Order Details")
        header_layout = QGridLayout(header_group)
        
        self.supplier_label = QLabel()
        self.invoice_no_label = QLabel()
        self.invoice_date_label = QLabel()
        self.status_label = QLabel()
        self.total_amount_label = QLabel()
        
        # Style critical fields
        self.status_label.setStyleSheet("font-weight: bold; font-size: 11pt;")
        self.total_amount_label.setStyleSheet("font-weight: bold; font-size: 12pt; color: #495057;")
        
        header_layout.addWidget(QLabel("Supplier:"), 0, 0); header_layout.addWidget(self.supplier_label, 0, 1)
        header_layout.addWidget(QLabel("Invoice No:"), 1, 0); header_layout.addWidget(self.invoice_no_label, 1, 1)
        header_layout.addWidget(QLabel("Invoice Date:"), 2, 0); header_layout.addWidget(self.invoice_date_label, 2, 1)
        
        header_layout.addWidget(QLabel("Status:"), 0, 2); header_layout.addWidget(self.status_label, 0, 3)
        header_layout.addWidget(QLabel("Order Total:"), 1, 2); header_layout.addWidget(self.total_amount_label, 1, 3)
        
        main_layout.addWidget(header_group)
        
        # 2. Line Items Table
        items_group = QGroupBox("Order Line Items")
        items_layout = QVBoxLayout(items_group)
        
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(7)
        self.items_table.setHorizontalHeaderLabels(["Product", "Batch No.", "Qty (Packs)", "Pack Cost ($)", "Line Total ($)", "Expiry", "Stock Qty"])
        self.items_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.items_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        items_layout.addWidget(self.items_table)
        main_layout.addWidget(items_group)

    def load_po_details(self):
        """Fetches and displays the PO header and line items."""
        
        # Call the new DB method
        po_details = self.db.get_po_details_for_viewer(self.order_id)
        
        if not po_details or not po_details['header']:
            QMessageBox.critical(self, "Error", f"Could not find Purchase Order #{self.order_id}.")
            return
            
        header = po_details['header']
        items = po_details['items']
        
        # 1. Populate Header
        self.supplier_label.setText(header['supplier_name'] or 'N/A')
        self.invoice_no_label.setText(header['invoice_number'] or 'N/A')
        self.invoice_date_label.setText(header['invoice_date'] or 'N/A')
        self.status_label.setText(header['status'])
        self.total_amount_label.setText(f"${header['total_invoice_amount']:.2f}")

        # 2. Populate Line Items
        self.items_table.setRowCount(len(items))
        
        for row_num, item in enumerate(items):
            # Check if this PO item has associated stock batches
            stock_qty = self.db.get_active_stock_for_purchase_item(item['p_item_id'])
            
            data = [
                item['product_name'], item['batch_number'], f"{item['pack_quantity']:.2f}",
                f"{item['pack_cost']:.2f}", f"{item['line_total']:.2f}", item['expiry_date'],
                f"{stock_qty:.2f} Packs"
            ]
            
            for col, value in enumerate(data):
                item_widget = QTableWidgetItem(value)
                # Highlight if stock is gone
                if col == 6 and stock_qty <= 0.001 and header['status'] != 'Voided':
                     item_widget.setBackground(QColor(255, 200, 200)) # Light Red
                
                self.items_table.setItem(row_num, col, item_widget)
                
        self.items_table.resizeColumnsToContents()
        self.items_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

# ==============================================================================
# NEW: SUPPLIER DETAIL DIALOG (Accessed via Supplier Master Tab)
# ==============================================================================

# ==============================================================================
# 4. SUPPLIER WIDGETS - SupplierDetailDialog (MODIFIED: Added PO Double-Click)
# ==============================================================================

# ==============================================================================
# 4. SUPPLIER WIDGETS - SupplierDetailDialog (FINAL MODIFICATION: Added Status Column)
# ==============================================================================

# ==============================================================================
# 4. SUPPLIER WIDGETS - SupplierDetailDialog (FINAL MODIFICATION: Added Products Tab)
# ==============================================================================

class SupplierDetailDialog(QDialog):
    """Shows ledger, contacts, and transaction history for a single supplier."""
    
    def __init__(self, db, supplier_name, parent=None):
        super().__init__(parent)
        self.db = db
        self.supplier_name = supplier_name
        self.setWindowTitle(f"Supplier Ledger & History: {supplier_name}")
        self.setMinimumSize(900, 600)
        self._setup_ui()
        self.load_supplier_data()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # --- 1. Summary and Tabs ---
        summary_h_layout = QHBoxLayout()
        self.contact_info_label = QLabel("Loading Contact Info...")
        self.balance_label = QLabel("BALANCE: $0.00")
        
        self.balance_label.setStyleSheet("font-size: 16pt; font-weight: bold; padding: 10px; background-color: #E9ECEF;")
        
        summary_h_layout.addWidget(self.contact_info_label)
        summary_h_layout.addWidget(self.balance_label)
        summary_h_layout.setStretch(0, 1)
        summary_h_layout.setStretch(1, 0)
        main_layout.addLayout(summary_h_layout)

        self.tab_widget = QTabWidget()
        
        # --- Tab 1: Products Ordered (NEW TAB) ---
        self.products_tab = QWidget()
        self.products_layout = QVBoxLayout(self.products_tab)
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels(["Product Name", "Class/Type", "Latest Cost ($)", "Last Order Date", "Unit Type"])
        self.products_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.products_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.products_layout.addWidget(QLabel("List of items previously ordered from this supplier:"))
        self.products_layout.addWidget(self.products_table)
        self.tab_widget.addTab(self.products_tab, "Products Ordered")
        
        # --- Tab 2: Purchase Orders ---
        self.po_tab = QWidget()
        self.po_layout = QVBoxLayout(self.po_tab)
        self.po_table = QTableWidget()
        self.po_table.setColumnCount(8) 
        self.po_table.setHorizontalHeaderLabels(["Order ID", "Invoice No", "Date", "Total Amt ($)", "Paid Amt ($)", "Credit ($)", "Pending ($)", "Status"])
        self.po_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.po_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.po_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.po_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.po_table.setColumnHidden(0, True) 
        
        self.po_table.doubleClicked.connect(self.view_purchase_order_details) 

        self.po_layout.addWidget(QLabel("Double-click an Order ID row to view the full Purchase Order details."))
        self.po_layout.addWidget(self.po_table)
        self.tab_widget.addTab(self.po_tab, "Purchase Orders")

        # --- Tab 3: Payments ---
        self.payments_tab = QWidget()
        self.payments_layout = QVBoxLayout(self.payments_tab)
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(5)
        self.payments_table.setHorizontalHeaderLabels(["Payment ID", "Date", "Amount ($)", "Method", "Related PO ID"])
        self.payments_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.payments_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.payments_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.payments_table.setColumnHidden(0, True) 
        self.payments_layout.addWidget(self.payments_table)
        self.tab_widget.addTab(self.payments_tab, "Payments Made")
        
        # --- Tab 4: Returns (Supplier Credits) ---
        self.returns_tab = QWidget()
        self.returns_layout = QVBoxLayout(self.returns_tab)
        self.returns_table = QTableWidget()
        self.returns_table.setColumnCount(4)
        self.returns_table.setHorizontalHeaderLabels(["Return Date", "Credit Value ($)", "Reason", "Related PO ID"])
        self.returns_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.returns_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.returns_layout.addWidget(self.returns_table)
        self.tab_widget.addTab(self.returns_tab, "Return Credits")
        
        main_layout.addWidget(self.tab_widget)
        
    def load_supplier_data(self):
        """Fetches and displays contact info, balance, POs, and payments."""
        
        # 1. Load Contact Info
        self.db.cursor.execute("SELECT contact_person, phone, email, address FROM supplier_contact WHERE supplier_name = ?", (self.supplier_name,))
        contact_data = self.db.cursor.fetchone()
        
        if contact_data:
            contact, phone, email, address = contact_data
            info_text = f"Contact: {contact or 'N/A'} | Phone: {phone or 'N/A'} | Email: {email or 'N/A'}\nAddress: {address or 'N/A'}"
            self.contact_info_label.setText(info_text)
        else:
            self.contact_info_label.setText("Contact information not set in Supplier Master tab.")

        # 2. Load POs (Orders Tab)
        self.db.cursor.execute("""
            SELECT order_id, invoice_number, order_date, total_invoice_amount, status
            FROM purchase_orders 
            WHERE supplier_name = ?
            ORDER BY order_date DESC
        """, (self.supplier_name,))
        
        all_orders = self.db.cursor.fetchall()
        po_data_list = []
        total_pending_balance = 0.0

        for po_id, inv_no, date, total_amount, status in all_orders:
            self.db.cursor.execute("SELECT COALESCE(SUM(amount_paid), 0.0) FROM supplier_payments WHERE order_id = ?", (po_id,))
            total_paid = self.db.cursor.fetchone()[0] or 0.0
            total_credit = self.db.get_order_returns_credit(po_id)
            net_paid = total_paid + total_credit
            pending = max(0.0, total_amount - net_paid)
            
            total_pending_balance += pending
            
            po_data_list.append({
                'id': po_id, 'inv_no': inv_no, 'date': date, 'total': total_amount,
                'paid': total_paid, 'credit': total_credit, 'pending': pending, 'status': status
            })
            
        self._populate_po_table(po_data_list)
        
        # 3. Load Payments
        self.db.cursor.execute("""
            SELECT T1.payment_id, T1.payment_date, T1.amount_paid, T1.payment_method, T1.order_id
            FROM supplier_payments AS T1
            LEFT JOIN purchase_orders AS T2 ON T1.order_id = T2.order_id
            WHERE T2.supplier_name = ?
            ORDER BY T1.payment_date DESC
        """, (self.supplier_name,))
        payments = self.db.cursor.fetchall()
        self._populate_payments_table(payments)
        
        # 4. Load Returns (supplier credits only)
        self.db.cursor.execute("""
            SELECT return_date, total_refund_value, reason, order_id
            FROM returns 
            WHERE supplier_name = ? AND reason NOT LIKE 'Customer Return%'
            ORDER BY return_date DESC
        """, (self.supplier_name,))
        returns = self.db.cursor.fetchall()
        self._populate_returns_table(returns)
        
        # 5. Load Products History (NEW)
        product_history = self.db.get_supplier_product_history(self.supplier_name)
        self._populate_products_table(product_history)
        
        # 6. Update Balance
        self.balance_label.setText(f"BALANCE PENDING: ${total_pending_balance:.2f}")
        if total_pending_balance > 0.001:
            self.balance_label.setStyleSheet("font-size: 16pt; font-weight: bold; padding: 10px; background-color: #FFD700;") # Yellow
        else:
             self.balance_label.setStyleSheet("font-size: 16pt; font-weight: bold; padding: 10px; background-color: #C2F0C2;") # Light Green


    def _populate_po_table(self, data_list):
        self.po_table.setRowCount(len(data_list))
        
        # Column mapping: 0: ID, 1: Inv No, 2: Date, 3: Total, 4: Paid, 5: Credit, 6: Pending, 7: Status
        for row_num, d in enumerate(data_list):
            
            data_list_for_table = [
                str(d['id']), d['inv_no'] or 'N/A', d['date'] or 'N/A', f"{d['total']:.2f}",
                f"{d['paid']:.2f}", f"{d['credit']:.2f}", f"{d['pending']:.2f}", d['status']
            ]
            
            for col_num, value in enumerate(data_list_for_table):
                item = QTableWidgetItem(value)
                
                # Color coding based on status
                if d['status'] == 'Voided':
                    item.setBackground(QColor(255, 200, 200)) # Light Red
                elif d['status'] == 'Paid':
                    item.setBackground(QColor(200, 255, 200)) # Light Green
                elif d['status'] == 'Received/Unpaid' and d['pending'] <= 0.001:
                    # Case where pending is zero but status not updated yet
                    item.setBackground(QColor(200, 255, 200)) 

                # Align money columns right
                if col_num in [3, 4, 5, 6]: 
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    
                self.po_table.setItem(row_num, col_num, item)
        self.po_table.resizeColumnsToContents()

    def _populate_payments_table(self, data):
        self.payments_table.setRowCount(len(data))
        for row_num, row_data in enumerate(data):
            # payment_id, payment_date, amount_paid, payment_method, order_id
            payment_id, date, amount, method, order_id = row_data
            
            data_list = [str(payment_id), date, f"{amount:.2f}", method, str(order_id) if order_id else 'N/A']
            
            for col_num, value in enumerate(data_list):
                item = QTableWidgetItem(value)
                if col_num == 2: item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.payments_table.setItem(row_num, col_num, item)
        self.payments_table.resizeColumnsToContents()

    def _populate_returns_table(self, data):
        self.returns_table.setRowCount(len(data))
        for row_num, row_data in enumerate(data):
            # return_date, total_refund_value, reason, order_id
            date, value, reason, order_id = row_data
            
            data_list = [date, f"{value:.2f}", reason, str(order_id) if order_id else 'N/A']
            
            for col_num, value in enumerate(data_list):
                item = QTableWidgetItem(value)
                if col_num == 1: item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.returns_table.setItem(row_num, col_num, item)
        self.returns_table.resizeColumnsToContents()

    def _populate_products_table(self, data):
        """Populates the new Products Ordered tab."""
        self.products_table.setRowCount(len(data))
        
        for row_num, row_data in enumerate(data):
            # product_id, name, unit_type, class_name, pack_cost_price, order_date
            product_id, name, unit_type, class_name, cost, date = row_data
            
            data_list = [
                name, 
                class_name or unit_type, 
                f"{cost:.2f}", 
                date, 
                unit_type
            ]
            
            for col_num, value in enumerate(data_list):
                item = QTableWidgetItem(value)
                if col_num == 2: item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.products_table.setItem(row_num, col_num, item)
                
        self.products_table.resizeColumnsToContents()
        self.products_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        
    def view_purchase_order_details(self, index):
        """Opens the POViewerDialog for the double-clicked Purchase Order."""
        row = index.row()
        po_id_item = self.po_table.item(row, 0) # Order ID is in the hidden Column 0
        
        if po_id_item:
            order_id = int(po_id_item.text())
            
            dialog = POViewerDialog(self.db, order_id, self)
            dialog.exec()
        else:
            QMessageBox.warning(self, "Selection Error", "Could not retrieve Order ID from the selected row.")

# ==============================================================================
# 4.5. NEW DIALOG TO VIEW SALE ITEM DETAILS
# ==============================================================================

class SaleDetailDialog(QDialog):
    """Dialog to display all line items and batch details for a single sale ID."""
    
    def __init__(self, db, sale_id, parent=None):
        super().__init__(parent)
        self.db = db
        self.sale_id = sale_id
        self.setWindowTitle(f"Sale Details: Invoice #{sale_id}")
        self.setMinimumSize(800, 450)
        self._setup_ui()
        self.load_sale_details()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Product Name", "Batch No.", "Expiry (M/Y)", "Qty (Units)", 
            "Net Unit Price ($)", "Cost Price ($)", "Subtotal ($)"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        main_layout.addWidget(QLabel(f"Line Items and Batch Details for Invoice #{self.sale_id}:"))
        main_layout.addWidget(self.table)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        main_layout.addWidget(self.close_button)

    def load_sale_details(self):
        query = """
        SELECT
            p.name,
            b.batch_number,
            b.expiry_date,
            si.quantity_sold,
            si.unit_price,
            si.cost_price_at_sale,
            (si.quantity_sold * si.unit_price) AS Subtotal
        FROM sale_items si
        JOIN products p ON si.product_id = p.product_id
        LEFT JOIN stock_batches b ON si.batch_id = b.batch_id
        WHERE si.sale_id = ?;
        """
        self.db.cursor.execute(query, (self.sale_id,))
        results = self.db.cursor.fetchall()
        
        self.table.setRowCount(len(results))
        
        for row_num, row_data in enumerate(results):
            # Data structure: Name, BatchNo, Expiry, Qty, NetPrice, CostPrice, Subtotal
            
            # Unit Cost Price (Cost price at sale is per base unit)
            unit_cost = row_data[5] if row_data[5] is not None else 0.00
            
            data_to_display = [
                row_data[0],                                 # Product Name
                row_data[1] or 'N/A',                        # Batch No.
                row_data[2] or 'N/A',                        # Expiry (M/Y)
                f"{row_data[3]:.2f}",                        # Qty (Units)
                f"{row_data[4]:.2f}",                        # Net Unit Price
                f"{unit_cost:.2f}",                          # Cost Price (Per Unit)
                f"{row_data[6]:.2f}"                         # Subtotal
            ]
            
            for col_num, value in enumerate(data_to_display):
                item = QTableWidgetItem(value)
                if col_num in [3, 4, 5, 6]:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row_num, col_num, item)
        
        self.table.resizeColumnsToContents()


# ==============================================================================
# NEW: SUPPLIER MANAGEMENT WIDGET (MASTER LIST & CONTACTS)
# ==============================================================================

# ==============================================================================
# NEW: SUPPLIER MANAGEMENT WIDGET (MASTER LIST & CONTACTS) - CORRECTED
# ==============================================================================

# ==============================================================================
# NEW: SUPPLIER MANAGEMENT WIDGET (MASTER LIST & CONTACTS) - MODIFIED
# ==============================================================================

class SupplierManagementWidget(QWidget):
    """Manages supplier contact information and links to the full ledger."""
    
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setLayout(QHBoxLayout())
        self._setup_ui()
        self.load_suppliers()

    def _setup_ui(self):
        # --- Left Panel: Input Form ---
        input_group = QGroupBox("Add/Update Supplier Contact")
        input_layout = QGridLayout(input_group)
        input_group.setFixedWidth(350)
        
        self.name_input = QLineEdit()
        self.contact_person_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QTextEdit()
        self.address_input.setMinimumHeight(50)
        self.address_input.setMaximumHeight(80)
        
        self.save_button = QPushButton("Save/Update Supplier")
        self.save_button.clicked.connect(self.save_supplier)
        self.save_button.setStyleSheet("background-color: #008080; color: white; padding: 10px;")

        self.clear_button = QPushButton("Clear Form")
        self.clear_button.clicked.connect(self.clear_form)
        self.clear_button.setProperty("class", "RedButton")
        
        input_layout.addWidget(QLabel("Supplier Name (Key):"), 0, 0); input_layout.addWidget(self.name_input, 0, 1)
        input_layout.addWidget(QLabel("Contact Person:"), 1, 0); input_layout.addWidget(self.contact_person_input, 1, 1)
        input_layout.addWidget(QLabel("Phone:"), 2, 0); input_layout.addWidget(self.phone_input, 2, 1)
        input_layout.addWidget(QLabel("Email:"), 3, 0); input_layout.addWidget(self.email_input, 3, 1)
        input_layout.addWidget(QLabel("Address:"), 4, 0); input_layout.addWidget(self.address_input, 4, 1)
        
        button_h_layout = QHBoxLayout()
        button_h_layout.addWidget(self.clear_button)
        button_h_layout.addWidget(self.save_button)
        input_layout.addLayout(button_h_layout, 5, 0, 1, 2)
        
        self.layout().addWidget(input_group)
        
        # --- Right Panel: Supplier List ---
        list_panel = QVBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter list by name, contact, or phone...")
        self.search_input.textChanged.connect(self.filter_suppliers)
        
        self.supplier_table = QTableWidget()
        self.supplier_table.setColumnCount(5)
        self.supplier_table.setHorizontalHeaderLabels(["Supplier Name", "Contact Person", "Phone", "Email", "Address"])
        self.supplier_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.supplier_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.supplier_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.supplier_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.supplier_table.cellClicked.connect(self.load_supplier_to_form)
        self.supplier_table.doubleClicked.connect(self.view_supplier_ledger_from_index)

        list_panel.addWidget(QLabel("Supplier Master List (Double-click to view ledger)"))
        list_panel.addWidget(self.search_input)
        list_panel.addWidget(self.supplier_table)
        
        self.layout().addLayout(list_panel, 1)
        
    def clear_form(self):
        self.name_input.clear()
        self.contact_person_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.name_input.setEnabled(True) # Re-enable key field
        self.name_input.setFocus()
        
    def load_suppliers(self):
        self.all_suppliers_data = self.db.get_all_suppliers_master()
        self.filter_suppliers()

    def filter_suppliers(self):
        search_text = self.search_input.text().strip().lower()
        filtered_data = []
        
        for row in self.all_suppliers_data:
            if not search_text or any(search_text in str(cell).lower() for cell in row):
                filtered_data.append(row)
                
        self._populate_supplier_table(filtered_data)
        
    def _populate_supplier_table(self, data):
        self.supplier_table.setRowCount(len(data))
        
        for row_num, row_data in enumerate(data):
            # T1.supplier_name, T1.contact_person, T1.phone, T1.email, T1.address
            for col_num, value in enumerate(row_data):
                item = QTableWidgetItem(str(value) or "N/A")
                self.supplier_table.setItem(row_num, col_num, item)
                
        self.supplier_table.resizeColumnsToContents()
        self.supplier_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

    # 🐛 FIXED: This method accepts row and column integers (int, int) from cellClicked
    def load_supplier_to_form(self, row, column):
        """Loads selected supplier data into the input form for editing."""
        self.name_input.setText(self.supplier_table.item(row, 0).text())
        self.contact_person_input.setText(self.supplier_table.item(row, 1).text())
        self.phone_input.setText(self.supplier_table.item(row, 2).text())
        self.email_input.setText(self.supplier_table.item(row, 3).text())
        self.address_input.setText(self.supplier_table.item(row, 4).text().replace("N/A", ""))
        self.name_input.setEnabled(False) # Prevent changing the key field during update

    def save_supplier(self):
        name = self.name_input.text().strip()
        contact = self.contact_person_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.toPlainText().strip()
        
        if not name:
            QMessageBox.warning(self, "Input Error", "Supplier Name is required.")
            self.name_input.setFocus()
            return
            
        success, message = self.db.add_or_update_supplier_master(name, contact, phone, email, address)
        
        if success:
            QMessageBox.information(self, "Success", f"Supplier '{name}' saved successfully.")
            self.load_suppliers() # Reload the list
            
            # --- CRITICAL UPDATE: Push new/updated supplier list back to OrderEntryWidget ---
            parent_widget = self.parent()
            if hasattr(parent_widget, 'order_entry_widget'):
                oe_widget = parent_widget.order_entry_widget
                new_supplier_names = self.db.get_supplier_names()
                
                # Re-set the underlying list and refresh the combo box
                oe_widget.supplier_names = new_supplier_names
                oe_widget.supplier_combo.clear()
                oe_widget.supplier_combo.addItems(["--- Select Existing Supplier ---"] + sorted(new_supplier_names))
                oe_widget.supplier_combo.setCurrentIndex(0)
                oe_widget.supplier_input.clear()
            # ----------------------------------------------------------------------------------

            self.clear_form()
        else:
            QMessageBox.critical(self, "Save Failed", message)

    # 🐛 FIXED: This method is used by doubleClicked(QModelIndex), which we will connect to.
    def view_supplier_ledger_from_index(self, index):
        """Opens the ledger dialog for the double-clicked supplier based on QModelIndex."""
        row = index.row()
        supplier_name = self.supplier_table.item(row, 0).text()
        
        dialog = SupplierDetailDialog(self.db, supplier_name, self)
        dialog.exec()

# ==============================================================================
# NEW: OLD BILL VIEWER WIDGET (COMPLETE REPLACEMENT WITH SOFT VOID AND FOLDER LOGIC)
# ==============================================================================

class OldBillViewerWidget(QWidget):
    """Allows searching for a past sale by ID, viewing details, and reprinting/voiding the bill."""
    
    # Shop Details (Needed for PDF generation functions)
    SHOP_NAME = "SHREE RAM MEDICAL"
    SHOP_ADDRESS = "Bus Stand Kamtha(BK), Tq Ardhapur, Dist Nanded, 431704"
    SHOP_DL_NO = "DL No: 20*346101 / 21*346102"
    SHOP_FSSAI = "FSSAI: 21521236000113"
    SHOP_PHONE = "Phone: 9822549178"
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        # Get user ID from MainWindow for voiding/logging
        main_window = self.window()
        self.user_id = main_window.user_id if hasattr(main_window, 'user_id') else 1 
        self.last_sale_data = None  
        self.setLayout(QVBoxLayout())
        self._setup_ui()
        self.reset_state()

    def reset_state(self):
        """Resets the state of the viewer after load or on startup."""
        self.last_sale_data = None
        self.invoice_input.clear()
        self.receipt_preview_label.setText("Enter an Invoice ID and click 'Fetch Details' to load the bill.")
        self.btn_fetch_details.setEnabled(True)
        self.btn_print_bill.setEnabled(False) 
        self.btn_void_sale.setEnabled(False) 
        self.lookup_status_label.setText("Status: Ready")
        self.invoice_input.setFocus()
        
    def _setup_ui(self):
        main_h_layout = QHBoxLayout()
        
        # Left Panel: Input and Actions
        left_panel = QVBoxLayout()
        left_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        title_label = QLabel("Invoice Management (Re-Print & Void)")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #008080; margin-bottom: 10px;")
        left_panel.addWidget(title_label)
        
        input_group = QGroupBox("Invoice Lookup & Actions")
        input_layout = QVBoxLayout(input_group)
        
        self.invoice_input = QLineEdit()
        self.invoice_input.setPlaceholderText("Enter Invoice ID (e.g., 1001)")
        self.invoice_input.setValidator(QIntValidator(1, 999999))
        self.invoice_input.returnPressed.connect(self.fetch_receipt_details)
        
        self.btn_fetch_details = QPushButton("Fetch Details & Load Preview")
        self.btn_fetch_details.clicked.connect(self.fetch_receipt_details)
        self.btn_fetch_details.setStyleSheet("background-color: #495057; color: white; padding: 10px; font-size: 11pt;")
        
        self.lookup_status_label = QLabel("Status: Ready")
        self.lookup_status_label.setStyleSheet("font-weight: bold; margin-top: 5px;")
        
        # Print Button
        self.btn_print_bill = QPushButton("Open Loaded Bill PDF")
        self.btn_print_bill.clicked.connect(self.print_loaded_receipt)
        self.btn_print_bill.setStyleSheet("background-color: #008080; color: white; padding: 15px; font-size: 12pt;")
        self.btn_print_bill.setEnabled(False) 
        
        # VOID Button (NEW)
        self.btn_void_sale = QPushButton("VOID Sale (Revert Stock & Keep Audit Trail)")
        self.btn_void_sale.clicked.connect(self.void_loaded_sale)
        self.btn_void_sale.setProperty("class", "RedButton")
        self.btn_void_sale.setEnabled(False)
        
        input_layout.addWidget(QLabel("Invoice ID:"))
        input_layout.addWidget(self.invoice_input)
        input_layout.addWidget(self.btn_fetch_details)
        input_layout.addWidget(self.lookup_status_label)
        input_layout.addWidget(QLabel("---"))
        input_layout.addWidget(self.btn_print_bill)
        input_layout.addWidget(self.btn_void_sale) 
        
        left_panel.addWidget(input_group)
        left_panel.addStretch(1)
        
        # Right Panel: Preview
        right_panel = QVBoxLayout()
        self.receipt_preview_label = QLabel("Invoice details will appear here.")
        self.receipt_preview_label.setWordWrap(True)
        self.receipt_preview_label.setStyleSheet("padding: 10px; background-color: #fff; font-family: 'Courier New', monospace; font-size: 8pt;")
        self.receipt_preview_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.receipt_preview_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        receipt_scroll_area = QScrollArea()
        receipt_scroll_area.setWidgetResizable(True)
        receipt_scroll_area.setWidget(self.receipt_preview_label)
        receipt_scroll_area.setFrameShape(QFrame.Shape.StyledPanel)
        
        right_panel.addWidget(QLabel("Invoice Details Preview:"))
        right_panel.addWidget(receipt_scroll_area)
        
        main_h_layout.addLayout(left_panel, 1)
        main_h_layout.addLayout(right_panel, 2)
        self.layout().addLayout(main_h_layout)

    # -----------------------------------------------------------
    # --- CORE METHODS (Fetch, Print, VOID) ---
    # -----------------------------------------------------------

    def fetch_receipt_details(self):
        """Fetches sale details and loads the preview."""
        
        self.btn_print_bill.setEnabled(False)  
        self.btn_void_sale.setEnabled(False)
        self.last_sale_data = None
        self.lookup_status_label.setText("Status: Fetching...")
        
        try:
            sale_id = int(self.invoice_input.text().strip())
        except ValueError:
            self.lookup_status_label.setText("Status: ❌ Invalid numeric Invoice ID.")
            QMessageBox.warning(self, "Input Error", "Please enter a valid numeric Invoice ID.")
            self.invoice_input.setFocus()
            return
            
        # 1. Fetch Sale Header Data (INCLUDING STATUS)
        query_sale = "SELECT transaction_date, total_amount, discount, payment_method, doctor_ref, patient_name, patient_address, status FROM sales WHERE id = ?"
        self.db.cursor.execute(query_sale, (sale_id,))
        sale_data_row = self.db.cursor.fetchone()
        
        if not sale_data_row:
            self.lookup_status_label.setText(f"Status: ❌ Invoice ID {sale_id} not found.")
            QMessageBox.critical(self, "Error", f"Invoice ID {sale_id} not found.")
            return

        date_time, total_amount, discount, payment_method, doctor_ref, patient_name, patient_address, status = sale_data_row
        original_date = date_time.split(' ')[0] 
        
        # 2. Handle Voided Status
        if status == 'Voided':
            self.lookup_status_label.setText(f"Status: ⛔ Invoice #{sale_id} is VOIDED (Total: $0.00).")
            QMessageBox.information(self, "Voided", f"Invoice #{sale_id} is already marked as VOIDED.")
            # Set data for preview, but disable print/void actions
            sale_data = {'sale_id': sale_id, 'subtotal': 0.0, 'discount': 0.0, 'final_total': 0.0, 
                         'payment_method': payment_method, 'patient_name': patient_name, 
                         'patient_address': patient_address, 'doctor_ref': doctor_ref, 
                         'transaction_date': original_date, 'status': status}
        else:
            # 3. Build the full data structure for an active sale
            sale_data = {
                'sale_id': sale_id, 'subtotal': total_amount + discount, 'discount': discount,
                'final_total': total_amount, 'payment_method': payment_method,
                'patient_name': patient_name, 'patient_address': patient_address,
                'doctor_ref': doctor_ref, 'transaction_date': original_date, 'status': status 
            }
            self.btn_print_bill.setEnabled(True) 
            self.btn_void_sale.setEnabled(True)
            self.lookup_status_label.setText(f"Status: ✅ Invoice #{sale_id} loaded. Ready to print or void (Current Total: ${total_amount:.2f}).")
        
        # 4. Store and Update Preview
        self.last_sale_data = sale_data
        self._update_receipt_preview(sale_data) 
        
    # --- MODIFIED: Print Loaded Receipt (Uses consistent print action) ---
    def print_loaded_receipt(self):
        """Prints the receipt using the cached data after it has been fetched."""
        if not self.last_sale_data or self.last_sale_data.get('status') == 'Voided':
            QMessageBox.warning(self, "Print Error", "Please fetch an ACTIVE invoice first.")
            return

        pdf_data = self._get_pdf_data(self.last_sale_data)
        # Calls the unified print action with trigger_print=True
        self.print_receipt_action(pdf_data, is_final_sale=True, is_reprint=True, trigger_print=True) 

    def void_loaded_sale(self):
        """Voids the currently loaded sale, reverting stock and marking the record."""
        if not self.last_sale_data or self.last_sale_data.get('status') == 'Voided':
            QMessageBox.warning(self, "Void Error", "No active invoice loaded to void.")
            return

        sale_id = self.last_sale_data['sale_id']
        total_amount = self.last_sale_data['final_total']
        
        reply = QMessageBox.question(self, 'CONFIRM VOID',
            f"ARE YOU SURE you want to **VOID** Invoice #{sale_id} (Original Total: ${total_amount:.2f})?\n\n"
            "The sale record will be marked 'Voided', stock will be fully restored, and the transaction value will be set to $0.00. This is the correct, auditable way to cancel a sale.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            result = self.db.soft_void_sale_transaction(sale_id, self.user_id)
            
            if result is True:
                QMessageBox.information(self, "Success", f"Invoice #{sale_id} successfully VOIDED and stock has been REVERTED.")
                self.reset_state()
                # Refresh main window dashboard/alerts
                main_window = self.window()
                if isinstance(main_window, MainWindow):
                    main_window._check_all_alerts()
                    main_window.show_dashboard_screen()
            else:
                QMessageBox.critical(self, "Void Failed", f"Void process failed. Reason: {result}")


    # -----------------------------------------------------------
    # --- REUSED PRINT UTILITIES (Uses consistent, safe printing) ---
    # -----------------------------------------------------------
    
    def _get_item_row_details(self, item):
        """Formats a single sale item for the receipt preview/PDF row. (REUSED)"""
        
        query_batch_info = "SELECT batch_number, expiry_date FROM stock_batches WHERE batch_id = ?"
        self.db.cursor.execute(query_batch_info, (item['batch_id'],))
        batch_info = self.db.cursor.fetchone()
        batch_number = batch_info[0] if batch_info else "N/A"
        expiry_date = batch_info[1] if batch_info else "N/A"
        
        query_company = "SELECT company FROM products WHERE product_id = ?"
        self.db.cursor.execute(query_company, (item['product_id'],))
        company = self.db.cursor.fetchone()
        mfg = company[0] if company and company[0] else "N/A"

        total_amount = round(item.get('quantity_sold', item.get('qty_base_units', 0.0)) * item.get('unit_price', item.get('price_per_base_unit', 0.0)), 2)
        exp_display = f"{expiry_date[5:]}/{expiry_date[:4]}" if len(expiry_date) >= 7 else expiry_date

        return [
            item.get('name', 'N/A'), mfg, f"{item.get('quantity_sold', item.get('qty_base_units', 0.0)):.1f}", f"{item.get('unit_price', item.get('price_per_base_unit', 0.0)):.2f}", 
            batch_number, exp_display, f"{total_amount:.2f}"
        ]

    def _get_pdf_data(self, sale_data):
        """Prepares consolidated data structure for the PDF generator."""
        
        query = """
        SELECT p.name, p.company, si.quantity_sold, si.unit_price, b.batch_number, b.expiry_date, si.quantity_sold * si.unit_price
        FROM sale_items si JOIN products p ON si.product_id = p.product_id LEFT JOIN stock_batches b ON si.batch_id = b.batch_id
        WHERE si.sale_id = ?
        """
        self.db.cursor.execute(query, (sale_data['sale_id'],))
        db_items = self.db.cursor.fetchall()

        items_data = []
        is_voided = sale_data.get('status') == 'Voided'
        
        for row in db_items:
            product_name, mfg, qty, rate, batch_number, expiry_date, total = row
            exp_display = f"{expiry_date[5:]}/{expiry_date[:4]}" if expiry_date and len(expiry_date) >= 7 else expiry_date or "N/A"
            
            line_total_display = "0.00" if is_voided else f"{total:.2f}"
            
            items_data.append([
                product_name, mfg or "N/A", f"{qty:.1f}", f"{rate:.2f}", batch_number or "N/A", exp_display, line_total_display
            ])
        
        amount_in_words = number_to_words(int(sale_data['final_total']))
        print_date = sale_data.get('transaction_date', datetime.date.today().strftime('%Y-%m-%d'))
        
        final_totals = {
            'subtotal': 0.00, 'discount': 0.00, 'final_total': 0.00
        } if is_voided else {
            'subtotal': sale_data['subtotal'], 'discount': sale_data['discount'], 'final_total': sale_data['final_total']
        }
        
        return {
            'sale_id': str(sale_data['sale_id']), 'total_amount': f"{final_totals['subtotal']:.2f}", 
            'discount': f"{final_totals['discount']:.2f}", 'grand_total': f"{final_totals['final_total']:.2f}",
            'payment_method': sale_data['payment_method'], 'amount_in_words': amount_in_words,
            'items': items_data, 'patient_name': sale_data.get('patient_name', 'CASH SALES'),
            'patient_address': sale_data.get('patient_address', 'N/A'), 'doctor_ref': sale_data.get('doctor_ref', 'N/A'),
            'print_date': print_date,
            'status': sale_data.get('status', 'Finalized') 
        }
        
    def _get_receipt_text(self, data):
        """Generates a plain text preview of the receipt. (REUSED)"""
        
        is_voided = data.get('status') == 'Voided'
        
        header = f"{self.SHOP_NAME}\n{self.SHOP_ADDRESS}\n{self.SHOP_DL_NO} | {self.SHOP_PHONE}\n"
        if is_voided:
             header += "\n*** VOIDED TRANSACTION ***\n"
        header += "="*40 + "\n"
        
        display_date = data.get('print_date', datetime.date.today().strftime('%Y-%m-%d'))
        header += f"Invoice: {data['sale_id']}     | Date: {display_date}\n" 
        header += f"Patient: {data.get('patient_name', 'CASH SALES')}\nDoctor: {data.get('doctor_ref', 'N/A')}\n" + "="*40 + "\n"
        
        items_text = f"{'Product':<15} {'Qty':>5} {'Rate':>8} {'Total':>8}\n" + "-"*40 + "\n"
        for item in data['items']:
            items_text += f"{item[0][:15]:<15} {item[2]:>5} {item[3]:>8} {item[6]:>8}\n"

        items_text += "-"*40 + "\n"
        items_text += f"{'Subtotal:':<30} {data['total_amount']:>8}\n"
        items_text += f"{'Discount:':<30} {data['discount']:>8}\n"
        items_text += f"{'GRAND TOTAL:':<30} {data['grand_total']:>8}\n" + "="*40 + "\n"
        
        words = data['amount_in_words'].replace('\n', ' ')
        items_text += f"IN WORDS: {words}\nPayment: {data['payment_method']}\n"
        
        return header + items_text

    def _update_receipt_preview(self, sale_data):
        """Updates the text preview window based on the sale data. (REUSED)"""
        pdf_data = self._get_pdf_data(sale_data)
        receipt_text = self._get_receipt_text(pdf_data)
        
        if len(receipt_text) > 2000:
            receipt_text = receipt_text[:2000] + "\n... (Preview truncated for length)"
            
        self.receipt_preview_label.setText(receipt_text)
        
    def print_receipt_action(self, pdf_data, is_final_sale, is_reprint=False, trigger_print=False):
        """Generates the PDF file and informs the user where it is saved."""
        
        id_part = str(pdf_data['sale_id'])
        
        # Use the new utility function to get the dynamic save path
        filename = _get_save_path(
            invoice_id=id_part, 
            invoice_date_str=pdf_data['print_date'],
            is_reprint=is_reprint
        )
            
        try:
            # External function call to ReportLab for dual-bill PDF
            generate_2bills_pdf(pdf_data, filename)
            
            # Extract only the base directory for display
            display_path = os.path.dirname(filename)
            
            status_msg = f"Invoice PDF successfully saved to **{display_path}**.\n"
            status_msg += "The file will be opened for printing/viewing."
            
            # --- CONSISTENT PRINT LOGIC (System Open) ---
            if trigger_print: 
                # *** CRITICAL FIX: Calls the global OS print utility ***
                _print_pdf_file_consistent(filename, self)
                status_msg = f"Invoice PDF saved and **FILE OPENED** for printing: **{display_path}**"
                
            QMessageBox.information(self, "PDF Generated", status_msg)

        except Exception as e:
            QMessageBox.critical(self, "Print Failed", f"Could not generate PDF. Error: {e}")
            print(f"PDF GENERATION ERROR: {e}")
            
    # --- DELETE/REPLACE THE OLD _print_pdf_file METHOD WITH THE SAFE IMPLEMENTATION ---
    def _print_pdf_file(self, filename):
        """
        THIS METHOD IS REPLACED with the safe, OS-native file opening mechanism 
        to avoid calling PDFtoPrinter.exe. 
        We use the global helper function for consistency and safety.
        """
        _print_pdf_file_consistent(filename, self)
# ==============================================================================
# NEW: PURCHASE ORDER DETAIL DIALOG
# ==============================================================================

class PurchaseOrderDetailDialog(QDialog):
    """Dialog to display all line items and batch details for a single PO."""
    
    def __init__(self, db, order_id, parent=None):
        super().__init__(parent)
        self.db = db
        self.order_id = order_id
        self.setWindowTitle(f"Purchase Order Details: PO #{order_id}")
        self.setMinimumSize(800, 450)
        self._setup_ui()
        self.load_po_details()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        self.header_label = QLabel("Loading PO Header...")
        self.header_label.setStyleSheet("font-weight: bold; font-size: 11pt; margin-bottom: 10px;")
        main_layout.addWidget(self.header_label)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Product Name", "Batch No.", "Qty Ordered (Packs)", "Pack Cost ($)", "Total Line Cost ($)"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        main_layout.addWidget(QLabel("Line Items:"))
        main_layout.addWidget(self.table)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        main_layout.addWidget(self.close_button)

    def load_po_details(self):
        po_data = self.db.get_purchase_order_details(self.order_id)
        
        if not po_data:
            self.header_label.setText(f"ERROR: PO #{self.order_id} not found.")
            return

        header = po_data['header']
        summary = po_data['summary']
        
        header_text = f"Supplier: {header['supplier']} | Inv No: {header['invoice_number']} | Date: {header['invoice_date']} | Status: {header['status']}\n"
        header_text += f"PO Total: ${header['total_invoice']:.2f} | Paid: ${summary['paid']:.2f} | Credit: ${summary['credit']:.2f} | Pending: ${summary['pending']:.2f}"
        self.header_label.setText(header_text)

        self.table.setRowCount(len(po_data['items']))
        
        for row_num, row_data in enumerate(po_data['items']):
            p_item_id, product_name, batch_number, qty_packs, pack_cost, units_per_pack, unit_type = row_data
            line_total = qty_packs * pack_cost
            
            data_to_display = [
                product_name,
                batch_number or 'N/A',
                f"{qty_packs:.2f} packs",
                f"{pack_cost:.2f}",
                f"{line_total:.2f}"
            ]
            
            for col_num, value in enumerate(data_to_display):
                item = QTableWidgetItem(value)
                if col_num in [2, 3, 4]:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row_num, col_num, item)
        
        self.table.resizeColumnsToContents()

class SaleDetailDialog(QDialog):
    """Dialog to display all line items and batch details for a single sale ID."""
    
    def __init__(self, db, sale_id, parent=None):
        super().__init__(parent)
        self.db = db
        self.sale_id = sale_id
        self.setWindowTitle(f"Sale Details: Invoice #{sale_id}")
        self.setMinimumSize(800, 450)
        self._setup_ui()
        self.load_sale_details()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Product Name", "Batch No.", "Expiry (M/Y)", "Qty (Units)", 
            "Net Unit Price ($)", "Cost Price ($)", "Subtotal ($)"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        main_layout.addWidget(QLabel(f"Line Items and Batch Details for Invoice #{self.sale_id}:"))
        main_layout.addWidget(self.table)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        main_layout.addWidget(self.close_button)

    def load_sale_details(self):
        query = """
        SELECT
            p.name,
            b.batch_number,
            b.expiry_date,
            si.quantity_sold,
            si.unit_price,
            si.cost_price_at_sale,
            (si.quantity_sold * si.unit_price) AS Subtotal
        FROM sale_items si
        JOIN products p ON si.product_id = p.product_id
        LEFT JOIN stock_batches b ON si.batch_id = b.batch_id
        WHERE si.sale_id = ?;
        """
        self.db.cursor.execute(query, (self.sale_id,))
        results = self.db.cursor.fetchall()
        
        self.table.setRowCount(len(results))
        
        for row_num, row_data in enumerate(results):
            # Data structure: Name, BatchNo, Expiry, Qty, NetPrice, CostPrice, Subtotal
            unit_cost = row_data[5] if row_data[5] is not None else 0.00
            
            data_to_display = [
                row_data[0],                                    # Product Name
                row_data[1] or 'N/A',                           # Batch No.
                row_data[2] or 'N/A',                           # Expiry (M/Y)
                f"{row_data[3]:.2f}",                           # Qty (Units)
                f"{row_data[4]:.2f}",                           # Net Unit Price
                f"{unit_cost:.2f}",                             # Cost Price (Per Unit)
                f"{row_data[6]:.2f}"                            # Subtotal
            ]
            
            for col_num, value in enumerate(data_to_display):
                item = QTableWidgetItem(value)
                if col_num in [3, 4, 5, 6]:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row_num, col_num, item)
        
        self.table.resizeColumnsToContents()

# ==============================================================================
# 4. REPORTS WIDGET (ANALYTICS) - COMPLETE REPLACEMENT
# ==============================================================================

# ==============================================================================
# MODIFIED: REPORTS WIDGET (SEPARATED SUPPLIER AND CUSTOMER RETURNS)
# ==============================================================================

# ==============================================================================
# MODIFIED: REPORTS WIDGET (SEPARATED RETURNS & DOUBLE-CLICK ON RETURN ID)
# ==============================================================================

# ==============================================================================
# MODIFIED: REPORTS WIDGET (SEPARATED RETURNS & DOUBLE-CLICK ON RETURN ID)
# ==============================================================================

class ReportsWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.main_layout = QVBoxLayout(self)
        self.current_report_type = None
        self._setup_controls()
        self._setup_table()
        
        self.current_report_data = []  

    def _setup_controls(self):
        controls_group = QGridLayout()
        
        self.report_selector = QComboBox()
        self.report_selector.addItem("Sales Transaction Report", "sales_summary")
        self.report_selector.addItem("Gross Margin Report (P/L)", "gross_margin")
        self.report_selector.addItem("Inventory Valuation", "inventory_value")
        self.report_selector.addItem("Low Reorder Stock", "reorder_report")  
        self.report_selector.addItem("Purchase Ledger (Payables)", "payables_report")
        self.report_selector.addItem("Payment History", "payment_history")  
        self.report_selector.addItem("Supplier Return History", "supplier_return_history") 
        self.report_selector.addItem("Customer Return History", "customer_return_history") # NEW DEDICATED REPORT
        self.report_selector.addItem("Audit Log Report", "audit_log")
        
        self.date_from = QDateEdit(QDate.currentDate().addMonths(-1))
        self.date_to = QDateEdit(QDate.currentDate())
        self.date_from.setCalendarPopup(True); self.date_to.setCalendarPopup(True)
        self.date_from.setDisplayFormat("yyyy-MM-dd"); self.date_to.setDisplayFormat("yyyy-MM-dd")
        
        self.generate_button = QPushButton("Generate Report")
        self.generate_button.clicked.connect(self.generate_report)
        self.generate_button.setStyleSheet("background-color: #008080; color: white;")

        self.export_button = QPushButton("Export to CSV")
        self.export_button.clicked.connect(self.export_to_csv)
        self.export_button.setEnabled(False)
        self.export_button.setStyleSheet("background-color: #6C757D; color: white;")
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Filter report results (e.g., product name, supplier, ID)...")
        self.search_bar.textChanged.connect(self._filter_report_table)
        self.search_bar.setEnabled(False)

        controls_group.addWidget(QLabel("Report Type:"), 0, 0); controls_group.addWidget(self.report_selector, 0, 1)
        controls_group.addWidget(QLabel("From:"), 1, 0); controls_group.addWidget(self.date_from, 1, 1)
        controls_group.addWidget(QLabel("To:"), 2, 0); controls_group.addWidget(self.date_to, 2, 1)
        controls_group.addWidget(self.generate_button, 0, 2, 1, 1); controls_group.addWidget(self.export_button, 1, 2, 1, 1)
        controls_group.addWidget(QLabel("Search/Filter:"), 3, 0); controls_group.addWidget(self.search_bar, 3, 1, 1, 2)


        self.main_layout.addLayout(controls_group)
        
        self.total_summary_label = QLabel("Summary: N/A")
        self.total_summary_label.setStyleSheet("font-weight: bold; padding: 10px; background-color: #E9ECEF; border-radius: 4px;")
        self.main_layout.addWidget(self.total_summary_label)

    def _setup_table(self):
        self.report_table = QTableWidget()
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.report_table.doubleClicked.connect(self.handle_table_double_click)
        self.report_table.horizontalHeader().sectionClicked.connect(self._handle_sort_request)
        
        self.main_layout.addWidget(self.report_table)
        
    def _handle_sort_request(self, logical_index):
        """Sorts the table based on the column header clicked."""
        current_sort_column = self.report_table.horizontalHeader().sortIndicatorSection()
        current_sort_order = self.report_table.horizontalHeader().sortIndicatorOrder()
        
        if current_sort_column == logical_index and current_sort_order == Qt.SortOrder.AscendingOrder:
            new_order = Qt.SortOrder.DescendingOrder
        else:
            new_order = Qt.SortOrder.AscendingOrder
            
        self.report_table.sortByColumn(logical_index, new_order)
        self.report_table.horizontalHeader().setSortIndicator(logical_index, new_order)

    def generate_report(self):
        report_type = self.report_selector.currentData()
        date_start = self.date_from.date().toString("yyyy-MM-dd")
        date_end = self.date_to.date().toString("yyyy-MM-dd")
        
        self.report_table.setRowCount(0); self.report_table.setColumnCount(0)
        self.total_summary_label.setText("Summary: Generating...")
        self.current_report_type = report_type
        self.current_report_data = []  
        self.search_bar.setEnabled(True)  
        self.report_table.horizontalHeader().setSortIndicator(-1, Qt.SortOrder.AscendingOrder)

        if report_type == "sales_summary": self.current_report_data = self._generate_sales_summary(date_start, date_end)
        elif report_type == "gross_margin": self.current_report_data = self._generate_gross_margin_report(date_start, date_end)
        elif report_type == "inventory_value": self.current_report_data = self._generate_inventory_valuation()
        elif report_type == "reorder_report": self.current_report_data = self._generate_reorder_report()
        elif report_type == "payables_report": self.current_report_data = self._generate_payables_report()
        elif report_type == "payment_history": self.current_report_data = self._generate_supplier_payments_history(date_start, date_end)
        elif report_type == "supplier_return_history": self.current_report_data = self._generate_return_history(date_start, date_end, is_customer_return=False)
        elif report_type == "customer_return_history": self.current_report_data = self._generate_return_history(date_start, date_end, is_customer_return=True)
        elif report_type == "audit_log": self.current_report_data = self._generate_audit_log_report()
            
        self._populate_report_table(self.current_report_data)

        self.export_button.setEnabled(self.report_table.rowCount() > 0)
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        if self.current_report_type == "sales_summary":
            self.report_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        elif self.current_report_type in ["gross_margin", "inventory_value", "supplier_return_history", "customer_return_history", "payment_history", "audit_log"]:
            self.report_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)


    def _filter_report_table(self):
        """Filters the currently stored report data based on the search bar text."""
        search_text = self.search_bar.text().strip().lower()
        
        if not self.current_report_data: return

        if not search_text:
            self._populate_report_table(self.current_report_data)
            return

        filtered_data = []
        for row_data in self.current_report_data:
            if any(search_text in str(cell).lower() for cell in row_data):
                filtered_data.append(row_data)

        self._populate_report_table(filtered_data, is_filtered=True)
        
    def _populate_report_table(self, data, is_filtered=False):
        """Populates the QTableWidget with the provided list of data."""
        
        if not data:
            self.report_table.setRowCount(0)
            if is_filtered:
                self.total_summary_label.setText("Summary: No results found matching the filter criteria.")
            return

        self.report_table.setRowCount(len(data))
        total_sum_value = 0.0
        
        # --- SALES SUMMARY ---
        if self.current_report_type == "sales_summary":
            for row_num, row_data in enumerate(data):
                invoice_status = row_data[5]
                final_amount = row_data[2]
                color = QColor(255, 255, 255) if invoice_status == 'Finalized' else QColor(255, 200, 200)
                if invoice_status == 'Finalized': total_sum_value += final_amount
                
                for col_num, value in enumerate(row_data):
                    item = QTableWidgetItem(f"{value:.2f}" if col_num in [2, 3] else str(value))
                    item.setBackground(color)
                    if col_num in [2, 3]: item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    self.report_table.setItem(row_num, col_num, item)
            
            if not is_filtered:
                self.total_summary_label.setText(f"Summary: Total Finalized Revenue: ${total_sum_value:.2f}. Double-click Invoice No. for line items.")

        # --- GROSS MARGIN ---
        elif self.current_report_type == "gross_margin":
            total_revenue = 0.0
            total_cogs = 0.0
            for row_num, row_data in enumerate(data):
                name, class_name, revenue, cogs, company = row_data
                margin = revenue - cogs
                margin_percent = (margin / revenue) * 100 if revenue > 0 else 0.0
                total_sum_value += margin
                total_revenue += revenue
                total_cogs += cogs
                
                display_data = [name, class_name, company, f"{revenue:.2f}", f"{cogs:.2f}", f"{margin:.2f}", f"{margin_percent:.2f}%"]
                
                for col_num, value in enumerate(display_data):
                    item = QTableWidgetItem(str(value))
                    if col_num in [3, 4, 5, 6]: item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    self.report_table.setItem(row_num, col_num, item)

            if not is_filtered:
                self.total_summary_label.setText(f"Summary (Finalized Sales Only): Total Revenue: ${total_revenue:.2f} | Total COGS: ${total_cogs:.2f} | Gross Margin: ${total_sum_value:.2f}")

        # --- INVENTORY VALUATION ---
        elif self.current_report_type == "inventory_value":
            for row_num, row_data in enumerate(data):
                name, total_packs, pack_cost, total_value, units_per_pack, unit_type = row_data
                total_sum_value += total_value
                
                pack_unit_display = 'Strips' if unit_type in ['TABLET', 'CAPSULE'] else unit_type.capitalize() + 's' if unit_type not in ['SYRUP', 'OINTMENT', 'MISCELLANEOUS'] else unit_type.capitalize()
                
                display_data = [name, f"{total_packs:.2f} {pack_unit_display}", unit_type, f"{pack_cost:.2f}", f"{total_value:.2f}"]
                
                for col_num, value in enumerate(display_data):
                    item = QTableWidgetItem(str(value))
                    if col_num in [3, 4]: item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    self.report_table.setItem(row_num, col_num, item)
            
            if not is_filtered:
                self.total_summary_label.setText(f"Summary: Total Current Inventory COST Value: ${total_sum_value:.2f}")

        # --- LOW REORDER STOCK ---
        elif self.current_report_type == "reorder_report":
             for row_num, row_data in enumerate(data):
                 name, stock, reorder, unit_type, supplier = row_data
                 color = QColor(255, 200, 200) if stock < 0.001 else QColor(255, 255, 200)
                 pack_unit_display = 'Strips' if unit_type in ['TABLET', 'CAPSULE'] else unit_type.capitalize() + 's' if unit_type not in ['SYRUP', 'OINTMENT', 'MISCELLANEOUS'] else unit_type.capitalize()
                 
                 data_display = [name, f"{stock:.2f} {pack_unit_display}", f"{reorder:.2f} {pack_unit_display}", unit_type, supplier]
                 
                 for col in range(len(data_display)):
                     q_item = QTableWidgetItem(data_display[col])
                     q_item.setBackground(color)
                     self.report_table.setItem(row_num, col, q_item)
             
             if not is_filtered:
                 self.total_summary_label.setText(f"Summary: {len(data)} items are below or at their reorder point.")
        
        # --- PAYABLES REPORT ---
        elif self.current_report_type == "payables_report":
            for row_num, row_data in enumerate(data):
                pending_amount = row_data[7]
                total_sum_value += pending_amount
                
                data_display = [str(row_data[0]), row_data[1], row_data[2], row_data[3]] + [f"{v:.2f}" for v in row_data[4:]]
                
                for col, value in enumerate(data_display):
                    item = QTableWidgetItem(value)
                    if col in [4, 5, 6, 7]: item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    self.report_table.setItem(row_num, col, item)
            
            if not is_filtered:
                self.total_summary_label.setText(f"Summary: Total Outstanding Payables: ${total_sum_value:.2f}. Double-click Order ID for line items.")

        # --- PAYMENT HISTORY ---
        elif self.current_report_type == "payment_history":
            for row_num, row_data in enumerate(data):
                supplier_name = row_data[2]
                amount_paid = row_data[3]
                total_sum_value += amount_paid
                
                data_display = [
                    str(row_data[0]), str(row_data[8]) if row_data[8] else 'N/A', row_data[1], 
                    supplier_name or 'N/A', f"{amount_paid:.2f}", row_data[4], 
                    row_data[5] or 'N/A', row_data[6] or 'N/A', row_data[7] or 'N/A'
                ]
                
                for col_num, value in enumerate(data_display):
                    item = QTableWidgetItem(value)
                    if col_num == 4: item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    self.report_table.setItem(row_num, col_num, item)

            if not is_filtered:
                self.total_summary_label.setText(f"Summary: Total Payments Recorded: ${total_sum_value:.2f}. Double-click Invoice ID for line items.")

        # --- SUPPLIER OR CUSTOMER RETURN HISTORY ---
        elif self.current_report_type in ["supplier_return_history", "customer_return_history"]:
            total_sum_value = 0.0
            
            for row_num, row_data in enumerate(data):
                total_refund = row_data[6]
                total_sum_value += total_refund
                
                # Highlight customer returns in light cyan, supplier returns in light gray
                color = QColor(200, 255, 255) if self.current_report_type == "customer_return_history" else QColor(240, 240, 240)
                
                data_display = [
                    row_data[0], row_data[1], row_data[2], row_data[3], f"{row_data[4]:.2f}", 
                    f"{row_data[5]:.2f}", f"{total_refund:.2f}", row_data[7], row_data[8], str(row_data[9]) if row_data[9] else 'N/A'
                ]
                
                for col, value in enumerate(data_display):
                    item = QTableWidgetItem(value)
                    item.setBackground(color)
                    if col in [4, 5, 6]: item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    self.report_table.setItem(row_num, col, item)

            if not is_filtered:
                self.total_summary_label.setText(f"Summary: Total Recorded Refund Value: ${total_sum_value:.2f}")


        # --- AUDIT LOG ---
        elif self.current_report_type == "audit_log":
            for row_num, row_data in enumerate(data):
                for col_num, value in enumerate(row_data):
                    self.report_table.setItem(row_num, col_num, QTableWidgetItem(str(value)))
            
            if not is_filtered:
                self.total_summary_label.setText(f"Summary: Displaying last {len(data)} audit log entries.")
        
        self.report_table.resizeColumnsToContents()
        self.report_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)


    # --- DATA FETCHING METHODS ---
    
    def _generate_audit_log_report(self):
        query = """
        SELECT timestamp, username, action, context_id, details
        FROM audit_log
        ORDER BY timestamp DESC
        LIMIT 500;
        """
        self.db.cursor.execute(query)
        results = self.db.cursor.fetchall()
        headers = ["Timestamp", "User", "Action Type", "Context ID", "Details"]
        self.report_table.setColumnCount(len(headers)); self.report_table.setHorizontalHeaderLabels(headers)
        return results

    def _generate_sales_summary(self, date_start, date_end):
        query = """
        SELECT s.id, s.transaction_date, s.total_amount, s.discount, s.payment_method, s.status, s.patient_name, s.doctor_ref
        FROM sales s  
        WHERE DATE(s.transaction_date) BETWEEN ? AND ?
        ORDER BY s.transaction_date DESC
        """
        self.db.cursor.execute(query, (date_start, date_end))
        results = self.db.cursor.fetchall()
        headers = ["Invoice No. (Dbl-Click)", "Date/Time", "Total Amount ($)", "Discount ($)", "Payment Method", "Status", "Patient Name", "Doctor Ref"]
        self.report_table.setColumnCount(len(headers)); self.report_table.setHorizontalHeaderLabels(headers)
        return results
        
    def _generate_gross_margin_report(self, date_start, date_end):
        query = """
        SELECT  
            p.name, c.name,  
            SUM(si.quantity_sold * si.unit_price) AS TotalRevenue,  
            SUM(si.quantity_sold * si.cost_price_at_sale) AS TotalCOGS,  
            p.company
        FROM sale_items si
        JOIN sales s ON si.sale_id = s.id
        JOIN products p ON si.product_id = p.product_id
        LEFT JOIN classes c ON p.class_id = c.class_id
        WHERE DATE(s.transaction_date) BETWEEN ? AND ? AND s.status = 'Finalized'
        GROUP BY p.product_id  
        ORDER BY TotalRevenue DESC;
        """
        self.db.cursor.execute(query, (date_start, date_end))
        results = self.db.cursor.fetchall()
        headers = ["Product Name", "Class", "Company", "Revenue ($)", "COGS ($)", "Gross Margin ($)", "Margin %"]
        self.report_table.setColumnCount(len(headers)); self.report_table.setHorizontalHeaderLabels(headers)
        return results

    def _generate_inventory_valuation(self):
        query = """
        SELECT  
            p.name, 
            SUM(b.stock_quantity) AS TotalPacks, 
            MIN(b.pack_cost_price) AS LowestPackCost,
            SUM(b.stock_quantity * b.pack_cost_price) AS TotalCostValue,  
            p.units_per_pack, 
            p.unit_type
        FROM products p
        JOIN stock_batches b ON p.product_id = b.product_id
        WHERE b.stock_quantity > 0 AND b.expiry_date >= STRFTIME('%Y-%m', 'now')  
        GROUP BY p.product_id  
        ORDER BY TotalCostValue DESC
        """
        self.db.cursor.execute(query)
        results = self.db.cursor.fetchall()
        headers = ["Product Name", "Total Packs", "Unit Type", "Pack Cost Price", "Total Cost Value ($)"]
        self.report_table.setColumnCount(len(headers)); self.report_table.setHorizontalHeaderLabels(headers)
        return results

    def _generate_reorder_report(self):
        query = """
        WITH CurrentStock AS (
            SELECT product_id, SUM(stock_quantity) AS TotalStock
            FROM stock_batches
            WHERE expiry_date >= STRFTIME('%Y-%m', 'now')
            GROUP BY product_id
        )
        SELECT p.name, COALESCE(cs.TotalStock, 0.0), p.reorder_point, p.unit_type, p.supplier
        FROM products p
        LEFT JOIN CurrentStock cs ON p.product_id = cs.product_id
        WHERE COALESCE(cs.TotalStock, 0.0) <= p.reorder_point
        ORDER BY p.name ASC
        """
        self.db.cursor.execute(query)
        results = self.db.cursor.fetchall()
        headers = ["Product Name", "Current Stock (Packs)", "Reorder Point (Packs)", "Unit Type", "Supplier"]
        self.report_table.setColumnCount(len(headers)); self.report_table.setHorizontalHeaderLabels(headers)
        return results

    def _generate_payables_report(self):
        invoices = self.db.get_supplier_pending_invoices()
        
        results = []
        for inv in invoices:
            self.db.cursor.execute("SELECT invoice_date, status FROM purchase_orders WHERE order_id = ?", (inv['order_id'],))
            data = self.db.cursor.fetchone()
            invoice_date = data[0]
            status = data[1]
            
            results.append((
                inv['order_id'], inv['supplier_name'], inv['invoice_number'], invoice_date,
                inv['total_invoice_amount'], inv['total_paid'], inv['return_credit'], inv['net_pending']
            ))
            
        headers = ["Order ID (Dbl-Click)", "Supplier", "Invoice No", "Date", "Invoice Total ($)", "Paid ($)", "Credit (Return) ($)", "Pending Balance ($)"]
        self.report_table.setColumnCount(len(headers)); self.report_table.setHorizontalHeaderLabels(headers)
        return results

    def _generate_supplier_payments_history(self, date_start, date_end):
        query = """
        SELECT  
            T1.payment_id,  
            T1.payment_date,  
            T3.supplier_name,  
            T1.amount_paid,  
            T1.payment_method,  
            T1.transaction_ref,  
            T1.notes,  
            T2.username,  
            T1.order_id
        FROM supplier_payments AS T1
        LEFT JOIN users AS T2 ON T1.user_id = T2.id
        LEFT JOIN purchase_orders AS T3 ON T1.order_id = T3.order_id  
        WHERE DATE(T1.payment_date) BETWEEN ? AND ?
        ORDER BY T1.payment_date DESC;
        """
        self.db.cursor.execute(query, (date_start, date_end))
        results = self.db.cursor.fetchall()
        headers = ["Payment ID", "Invoice ID (Dbl-Click)", "Date", "Supplier Name", "Amount Paid ($)", "Method", "Ref ID/Cheque", "Notes", "Recorded By"]
        self.report_table.setColumnCount(len(headers)); self.report_table.setHorizontalHeaderLabels(headers)
        return results

    def _generate_return_history(self, date_start, date_end, is_customer_return):
        """Fetches ONLY SUPPLIER Returns or ONLY CUSTOMER Returns based on flag."""
        
        # Filters based on the unique prefix used for customer returns
        condition = "r.supplier_name NOT LIKE 'Customer Return from Invoice %'" if not is_customer_return else "r.supplier_name LIKE 'Customer Return from Invoice %'"
        
        query = f"""
        SELECT  
            r.return_date, p.name, r.supplier_name, b.batch_number, 
            r.quantity_returned_packs, 
            r.cost_price_at_return, 
            r.total_refund_value, 
            r.reason, b.expiry_date, r.order_id   
        FROM returns r
        JOIN products p ON r.product_id = p.product_id
        JOIN stock_batches b ON r.batch_id = b.batch_id
        WHERE DATE(r.return_date) BETWEEN ? AND ? AND {condition}
        ORDER BY r.return_date DESC
        """
        self.db.cursor.execute(query, (date_start, date_end))
        results = self.db.cursor.fetchall()
        
        # Headers change dynamically based on the report type
        if is_customer_return:
             # order_id column holds the RETURN TRANSACTION ID
             headers = ["Return Date", "Product Name", "Invoice/Customer Ref", "Batch No.", "Qty (Packs)", "Unit Cost ($)", "Total Refund ($)", "Reason", "Batch Expiry", "Trans ID (Dbl-Click)"]
        else:
             headers = ["Return Date", "Product Name", "Supplier Name", "Batch No.", "Qty (Packs)", "Pack Cost ($)", "Total Refund ($)", "Reason", "Batch Expiry", "Linked Order ID"]
             
        self.report_table.setColumnCount(len(headers)); self.report_table.setHorizontalHeaderLabels(headers)
        return results

    # --- NEW DEDICATED METHODS FOR UI CALLS ---
    def _generate_customer_return_history(self, date_start, date_end):
        """Helper function for UI menu call."""
        return self._generate_return_history(date_start, date_end, is_customer_return=True)
        
    def _generate_supplier_return_history(self, date_start, date_end):
        """Helper function for UI menu call."""
        return self._generate_return_history(date_start, date_end, is_customer_return=False)
        
    # --- END DATA FETCHING METHODS ---

    def handle_table_double_click(self, index):
        if index.column() == 0 and self.current_report_type == "sales_summary":
            try:
                invoice_id_item = self.report_table.item(index.row(), 0)
                if invoice_id_item:
                    sale_id = int(invoice_id_item.text())
                    dialog = SaleDetailDialog(self.db, sale_id, self)
                    dialog.exec()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open sale details: {e}")

        elif index.column() == 0 and self.current_report_type == "payables_report":
            try:
                order_id_item = self.report_table.item(index.row(), 0)
                if order_id_item:
                    order_id = int(order_id_item.text())
                    dialog = PurchaseOrderDetailDialog(self.db, order_id, self)
                    dialog.exec()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open PO details: {e}")

        elif index.column() == 1 and self.current_report_type == "payment_history":
            try:
                po_id_item = self.report_table.item(index.row(), 1)
                if po_id_item and po_id_item.text() not in ['N/A', 'None']:
                    order_id = int(po_id_item.text())
                    dialog = PurchaseOrderDetailDialog(self.db, order_id, self)
                    dialog.exec()
                else:
                    QMessageBox.information(self, "No PO Link", "This payment is not linked to a specific Purchase Order ID.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open PO details: {e}")

        # --- DOUBLE-CLICK ON CUSTOMER RETURN TRANSACTION ID ---
        elif self.current_report_type == "customer_return_history":
            # The RETURN TRANSACTION ID is the last column (index 9)
            if index.column() == 9: 
                try:
                    return_trans_id_item = self.report_table.item(index.row(), 9)
                    
                    if return_trans_id_item and return_trans_id_item.text() not in ['N/A', 'None']:
                        return_trans_id = int(return_trans_id_item.text()) 
                        # Call the new Return Transaction Detail Dialog
                        dialog = ReturnTransactionDetailDialog(self.db, return_trans_id, self)
                        dialog.exec()
                    else:
                        QMessageBox.information(self, "No Details", "This return entry does not have an associated transaction ID.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not open return transaction details: {e}")

    def export_to_csv(self):
        if self.report_table.rowCount() == 0:
            QMessageBox.warning(self, "Export Error", "No data to export.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self,  
                                                     "Export Report to CSV",  
                                                     f"{self.report_selector.currentText().replace(' ', '_')}.csv",  
                                                     "CSV Files (*.csv)")

        if file_name:
            try:
                with open(file_name, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    headers = [self.report_table.horizontalHeaderItem(i).text() for i in range(self.report_table.columnCount())]
                    writer.writerow(headers)
                    
                    for row in range(self.report_table.rowCount()):
                        row_data = []
                        for col in range(self.report_table.columnCount()):
                            item = self.report_table.item(row, col)
                            row_data.append(item.text() if item is not None else "")
                        writer.writerow(row_data)
                        
                    QMessageBox.information(self, "Export Success", f"Report successfully exported to:\n{file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to save file: {e}")
# ==============================================================================
# 5. INVENTORY WIDGETS - MODIFIED AddProductDialog (Supplier/Company not required)
# ==============================================================================

# ==============================================================================
# 5. INVENTORY WIDGETS - AddProductDialog (MODIFIED: Removed Supplier/Company)
# ==============================================================================

# ==============================================================================
# 5. INVENTORY WIDGETS - AddProductDialog (RESTORED: Company Field)
# ==============================================================================

class AddProductDialog(QDialog):
    """Dialog for creating a NEW product master record only."""
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Add New Product Master Record")
        self.setFixedSize(600, 400) # Reverted to original height
        
        self.db.cursor.execute("SELECT class_id, name FROM classes ORDER BY name ASC")
        self.classes = self.db.cursor.fetchall()
        
        # Company names needed for autocompleter
        self.company_names = self.db.get_company_names() 
        
        self._setup_ui()
        self._setup_company_completer() # Re-added completer setup
        self.class_combo.currentIndexChanged.connect(self.update_units_per_pack_state)
        
    # --- Completer methods ---
    def _setup_company_completer(self):
        """Sets up QCompleter for the company input."""
        self.company_model = QStringListModel(self.company_names)
        self.company_completer = QCompleter(self.company_model)
        self.company_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.company_completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.company_input.setCompleter(self.company_completer)

    def update_units_per_pack_state(self):
        """Disables/enables Units Per Pack and sets default based on Class (now used as Unit Type)."""
        selected_class_name = self.class_combo.currentText().upper()
        is_strip_unit = selected_class_name in ['TABLET', 'CAPSULE']
        self.units_per_pack_input.setEnabled(is_strip_unit)
        
        if is_strip_unit:
            self.units_per_pack_input.setText("10")
            pack_label_text = "Units Per Pack (e.g., Tabs/Strip):"
        else:
            self.units_per_pack_input.setText("1")
            pack_label_text = "Units Per Pack (Set to 1):"
            
        self.units_per_pack_label.setText(pack_label_text)


    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        form_layout = QGridLayout()

        self.name_input = QLineEdit(); self.class_combo = QComboBox()
        for class_id, class_name in self.classes: self.class_combo.addItem(class_name, class_id)
        
        self.units_per_pack_input = QLineEdit("1")
        self.units_per_pack_input.setValidator(QIntValidator(1, 999))
        
        # --- RESTORED: Company Input ---
        self.company_input = QLineEdit() 
        self.formulation_input = QLineEdit()
        
        self.reorder_input = QLineEdit("10")
        self.reorder_input.setValidator(QIntValidator(1, 9999))
        
        self.units_per_pack_label = QLabel("Units Per Pack (Set to 1):") 

        # --- Layout Adjustment ---
        form_layout.addWidget(QLabel("Name:"), 0, 0); form_layout.addWidget(self.name_input, 0, 1)
        form_layout.addWidget(QLabel("Class/Unit Type:"), 1, 0); form_layout.addWidget(self.class_combo, 1, 1)
        
        form_layout.addWidget(self.units_per_pack_label, 2, 0); form_layout.addWidget(self.units_per_pack_input, 2, 1)
        
        # RESTORED ROW 3
        form_layout.addWidget(QLabel("Company (Optional):"), 3, 0); form_layout.addWidget(self.company_input, 3, 1) 
        
        # Supplier row is PERMANENTLY REMOVED
        
        form_layout.addWidget(QLabel("Reorder Packs:"), 4, 0); form_layout.addWidget(self.reorder_input, 4, 1) 
        
        self.btn_save = QPushButton("Save Product Master")
        self.btn_save.setStyleSheet("padding: 12px; font-size: 11pt; background-color: #008080; color: white;") 
        self.btn_save.clicked.connect(self.save_data)
        
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.btn_save)
        
        self.update_units_per_pack_state()


    def save_data(self):
        name = self.name_input.text().strip()
        class_id = self.class_combo.currentData()
        class_name = self.class_combo.currentText().upper()
        # supplier_name is explicitly hardcoded empty in query below
        company_name = self.company_input.text().strip() # RESTORED
        
        try:
            units_per_pack = int(self.units_per_pack_input.text())
            reorder = int(self.reorder_input.text() or 0)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Units per pack and Reorder must be valid integers.")
            return

        # Check required fields
        if not name or units_per_pack <= 0 or not class_id:
            QMessageBox.warning(self, "Input Error", "Name, Units per pack, and Class must be filled correctly.")
            return
            
        # Add company name to master list
        if company_name: self.db.add_company_name(company_name)

        try:
            with self.db.conn:  
                # MODIFIED QUERY: Supplier field is now set to an empty string ("")
                query = """INSERT INTO products (name, class_id, units_per_pack, unit_type, company, supplier, formulation, reorder_point) 
                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                self.db.cursor.execute(query, (name, class_id, units_per_pack, class_name, company_name, "", self.formulation_input.text(), reorder))
                product_id = self.db.cursor.lastrowid
            
            # NEW: Log Product Creation
            main_window = self.parent().parent()
            if hasattr(main_window, 'user_id'):
                user_info = self.db.cursor.execute("SELECT username FROM users WHERE id=?", (main_window.user_id,)).fetchone()
                username = user_info[0] if user_info else 'System'
                self.db.log_action(
                    main_window.user_id,
                    username,
                    'PRODUCT_CREATE',
                    product_id,
                    f"Name: {name}. Master record created. Prices/Supplier to be set in Purchasing."
                )
            
            QMessageBox.information(self, "Success", f"Product '{name}' saved successfully. **Supplier and Prices must be set in Purchasing/Receive Stock.**")
            self.accept()
            
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "DB Error", "Product name is already in use.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

# ==============================================================================
# 5. INVENTORY WIDGETS - ProductDetailDialog (MODIFIED: Removed Supplier/Company)
# ==============================================================================

# ==============================================================================
# 5. INVENTORY WIDGETS - ProductDetailDialog (RESTORED: Company Field)
# ==============================================================================

class ProductDetailDialog(QDialog):
    def __init__(self, db, product_id, parent=None):
        super().__init__(parent)
        self.db = db
        self.product_id = product_id
        self.original_product_name = ""
        self.setWindowTitle("Product Details & Batch Management")
        self.setMinimumSize(800, 600) # Restored original min height
        
        self.db.cursor.execute("SELECT class_id, name FROM classes ORDER BY name ASC")
        self.classes = self.db.cursor.fetchall()
        
        self.company_names = self.db.get_company_names() # Added company list
        
        self._setup_ui()
        self._setup_company_completer() # Re-added completer setup
        self.load_product_data()
        
    # --- Completer methods ---
    def _setup_company_completer(self):
        """Sets up QCompleter for the company input."""
        self.company_model = QStringListModel(self.company_names)
        self.company_completer = QCompleter(self.company_model)
        self.company_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.company_completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.company_input.setCompleter(self.company_completer)
    
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # --- 1. Product Master Details (Editable) ---
        master_group = QGroupBox("Product Master Details (Edit & Save)")
        master_layout = QGridLayout(master_group)
        
        self.name_input = QLineEdit()
        self.units_per_pack_input = QLineEdit()
        self.units_per_pack_input.setValidator(QIntValidator(1, 999))
        self.reorder_input = QLineEdit(); self.reorder_input.setValidator(QIntValidator(1, 9999))
        self.unit_type_label = QLabel("N/A") 
        
        self.class_combo = QComboBox()
        for class_id, class_name in self.classes: self.class_combo.addItem(class_name, class_id)
        
        # --- RESTORED: Company Input ---
        self.company_input = QLineEdit() 
        
        # --- Layout Adjustment ---
        master_layout.addWidget(QLabel("Name:"), 0, 0); master_layout.addWidget(self.name_input, 0, 1)
        master_layout.addWidget(QLabel("Class:"), 1, 0); master_layout.addWidget(self.class_combo, 1, 1)
        
        master_layout.addWidget(QLabel("Units/Pack:"), 2, 0); master_layout.addWidget(self.units_per_pack_input, 2, 1)
        master_layout.addWidget(QLabel("Base Unit Type (DB):"), 3, 0); master_layout.addWidget(self.unit_type_label, 3, 1)
        
        master_layout.addWidget(QLabel("Reorder Point:"), 0, 2); master_layout.addWidget(self.reorder_input, 0, 3)
        
        # RESTORED COMPANY INPUT
        master_layout.addWidget(QLabel("Company:"), 1, 2); master_layout.addWidget(self.company_input, 1, 3) 
        
        # Supplier is read-only information, fetched but not editable here
        self.supplier_display_label = QLabel("Loading...")
        master_layout.addWidget(QLabel("Supplier (Last PO):"), 2, 2); master_layout.addWidget(self.supplier_display_label, 2, 3) 
        
        self.btn_save_master = QPushButton("Save Master Info")
        self.btn_save_master.setStyleSheet("background-color: #6C757D; color: white;") 
        self.btn_save_master.clicked.connect(self.save_master_data)
        master_layout.addWidget(self.btn_save_master, 4, 3) 
        main_layout.addWidget(master_group)

        # --- 2. Batch Details (Read-Only List + Delete) --- 
        batch_group = QGroupBox("Active Stock Batches (FEFO Order)")
        batch_layout = QVBoxLayout(batch_group)
        
        self.batch_table = QTableWidget()
        self.batch_table.setColumnCount(7) 
        self.batch_table.setHorizontalHeaderLabels(["Batch ID", "Batch No.", "Received Date", "Expiry (M/Y)", "Qty (Packs)", "Qty (Units)", "Order ID"])
        self.batch_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.batch_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.batch_table.setColumnHidden(0, True) 
        self.batch_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.batch_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.batch_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.btn_delete_batch = QPushButton("Delete Selected Batch")
        self.btn_delete_batch.setProperty("class", "RedButton") 
        self.btn_delete_batch.clicked.connect(self.delete_selected_batch)
        
        batch_layout.addWidget(self.batch_table)
        batch_layout.addWidget(self.btn_delete_batch)
        main_layout.addWidget(batch_group)
    
    def load_product_data(self):
        # MODIFIED QUERY: Fetching all relevant fields 
        query_master = "SELECT name, class_id, units_per_pack, unit_type, reorder_point, supplier, company FROM products WHERE product_id = ?"
        self.db.cursor.execute(query_master, (self.product_id,))
        data = self.db.cursor.fetchone()
        
        if data:
            name, class_id, upp, ut, rop, supplier, company = data
            self.original_product_name = name
            
            self.name_input.setText(name)
            self.units_per_pack_input.setText(str(upp))
            self.reorder_input.setText(str(rop))
            self.unit_type_label.setText(ut)
            
            self.company_input.setText(company or '') # RESTORED COMPANY INPUT
            self.supplier_display_label.setText(supplier or 'N/A') # Read-only supplier display

            self.units_per_pack_input.setEnabled(ut in ['TABLET', 'CAPSULE'])
            
            index = self.class_combo.findData(class_id)
            if index != -1: self.class_combo.setCurrentIndex(index)
            
            self.load_batch_data(upp)

    def load_batch_data(self, units_per_pack):
        """Loads stock batches for the product, ordered by FEFO."""
        query_batches = """
        SELECT 
            T1.batch_id, 
            T1.batch_number, 
            T1.date_received, 
            T1.expiry_date, 
            T1.stock_quantity,
            T2.order_id
        FROM stock_batches T1
        LEFT JOIN purchase_items T2 ON T1.purchase_item_id = T2.p_item_id 
        WHERE T1.product_id = ? AND T1.stock_quantity > 0 
        ORDER BY T1.expiry_date ASC, T1.date_received ASC
        """
        self.db.cursor.execute(query_batches, (self.product_id,))
        batches = self.db.cursor.fetchall()
        
        self.batch_table.setRowCount(len(batches))
        today_yyyymm = datetime.date.today().strftime('%Y-%m')
        
        for row_num, batch in enumerate(batches):
            batch_id, batch_number, date_received, expiry_date, pack_qty, order_id = batch 
            base_unit_qty = int(pack_qty * units_per_pack)
            
            order_id_display = str(order_id) if order_id else "N/A"
            
            q_items = [
                QTableWidgetItem(str(batch_id)),
                QTableWidgetItem(batch_number), 
                QTableWidgetItem(date_received),
                QTableWidgetItem(expiry_date), 
                QTableWidgetItem(f"{pack_qty:.2f}"),
                QTableWidgetItem(str(base_unit_qty)),
                QTableWidgetItem(order_id_display)
            ]
            
            for col, item in enumerate(q_items):
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.batch_table.setItem(row_num, col, item)

            if expiry_date < today_yyyymm:
                for item in q_items:
                    item.setBackground(QColor(255, 200, 200))

        self.batch_table.resizeColumnsToContents()

    def save_master_data(self):
        new_name = self.name_input.text().strip()
        new_class_id = self.class_combo.currentData()
        new_unit_type = self.class_combo.currentText().upper()
        new_company = self.company_input.text().strip() # RESTORED
        
        try:
            new_reorder = int(self.reorder_input.text() or 0)
            new_upp = int(self.units_per_pack_input.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Reorder, and Units per pack must be valid numbers.")
            return

        if not new_name or new_upp <= 0 or not new_class_id:
            QMessageBox.warning(self, "Input Error", "Name, Units per pack, and Class must be filled correctly.")
            return

        if new_company: self.db.add_company_name(new_company) # Add company name to master list
        
        try:
            with self.db.conn:
                # MODIFIED QUERY: Re-included the company field, kept supplier empty string
                query = """UPDATE products SET name=?, class_id=?, units_per_pack=?, unit_type=?, reorder_point=?, company=? WHERE product_id=?"""
                self.db.cursor.execute(query, (new_name, new_class_id, new_upp, new_unit_type, new_reorder, new_company, self.product_id))
            
            # NEW: Log the Product Master Update event 
            main_window = self.parent().parent()
            user_info = self.db.cursor.execute("SELECT username FROM users WHERE id=?", (main_window.user_id,)).fetchone()
            username = user_info[0] if user_info else 'System'
            self.db.log_action(
                main_window.user_id,
                username,
                'PRODUCT_UPDATE',
                self.product_id,
                f"Updated master data for {self.original_product_name} -> {new_name}. Company: {new_company}"
            )

            QMessageBox.information(self, "Success", f"Product master data updated successfully.")
            self.original_product_name = new_name 
            self.load_product_data() # Reload to show changes
            
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "DB Error", "Product name is already in use by another item.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def delete_selected_batch(self):
        selected_rows = self.batch_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Deletion Error", "Please select a batch to delete.")
            return
            
        row_index = selected_rows[0].row()
        batch_id_item = self.batch_table.item(row_index, 0)
        pack_qty_item = self.batch_table.item(row_index, 4)

        batch_id = int(batch_id_item.text())
        pack_qty = pack_qty_item.text()

        # Check audit trail constraints
        self.db.cursor.execute("SELECT COUNT(*) FROM sale_items WHERE batch_id = ?", (batch_id,))
        sale_count = self.db.cursor.fetchone()[0]
        self.db.cursor.execute("SELECT COUNT(*) FROM returns WHERE batch_id = ?", (batch_id,))
        return_count = self.db.cursor.fetchone()[0]
        
        if sale_count > 0 or return_count > 0:
            QMessageBox.critical(self, "Deletion Forbidden", f"Batch ID {batch_id} has audit history ({sale_count} sales/{return_count} returns) and cannot be deleted.")
            return

        reply = QMessageBox.question(self, 'Confirm Batch Delete',
            f"Are you SURE you want to delete Batch ID {batch_id} for '{self.original_product_name}' (Qty: {pack_qty} Packs)? \n\nTHIS ACTION IS IRREVERSIBLE.", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                with self.db.conn:
                    self.db.cursor.execute("SELECT purchase_item_id FROM stock_batches WHERE batch_id = ?", (batch_id,))
                    p_item_id = self.db.cursor.fetchone()[0]
                    
                    self.db.cursor.execute("DELETE FROM stock_batches WHERE batch_id = ?", (batch_id,))
                    
                    if p_item_id is not None:
                        self.db.cursor.execute("SELECT COUNT(*) FROM stock_batches WHERE purchase_item_id = ?", (p_item_id,))
                        if self.db.cursor.fetchone()[0] == 0:
                            self.db.cursor.execute("DELETE FROM purchase_items WHERE p_item_id = ?", (p_item_id,))
                
                # NEW: Log the Batch Deletion event
                main_window = self.parent().parent()
                user_info = self.db.cursor.execute("SELECT username FROM users WHERE id=?", (main_window.user_id,)).fetchone()
                username = user_info[0] if user_info else 'System'
                self.db.log_action(
                    main_window.user_id,
                    username,
                    'BATCH_DELETE',
                    batch_id,
                    f"Deleted batch for {self.original_product_name}. Qty removed: {pack_qty}"
                )

                QMessageBox.information(self, "Success", f"Batch ID {batch_id} has been deleted.")
                
                self.load_product_data()
                
                if self.parent() and isinstance(self.parent().parent(), MainWindow):
                    inventory_widget = self.parent().parent().content_layout.itemAt(0).widget()
                    if isinstance(inventory_widget, InventoryWidget):
                        inventory_widget.load_product_master()
                
            except Exception as e:
                QMessageBox.critical(self, "Deletion Failed", f"Could not delete batch: {e}")

# ==============================================================================
# 5. INVENTORY WIDGETS - InventoryWidget (MODIFIED: Simplified Columns)
# ==============================================================================

class InventoryWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.main_inventory_layout = QVBoxLayout(self)
        
        self.content_stack = QWidget() 
        self.content_layout = QVBoxLayout(self.content_stack)
        
        # Add the content stack to the main layout, allowing it to stretch vertically
        self.main_inventory_layout.addWidget(self.content_stack, 1)
        
        self._create_permanent_elements() 
        self.load_product_master()

    def _create_permanent_elements(self):
        """Creates all UI elements, prioritizing vertical space for the table."""
        
        # --- 1. Controls (Top Button Panel) ---
        self.control_buttons_container = QWidget()
        self.control_layout = QHBoxLayout(self.control_buttons_container)
        self.control_layout.setContentsMargins(0, 0, 0, 0)

        self.btn_add_product = QPushButton("Add New Product Type")
        self.btn_add_batch = QPushButton("Receive New Stock (Purchasing)")
        self.btn_refresh_master = QPushButton("Refresh List")
        self.btn_delete_product = QPushButton("Delete Selected Product") 

        self.btn_add_product.clicked.connect(self.show_add_product_dialog)
        self.btn_add_product.setStyleSheet("background-color: #008080; color: white;") 
        self.btn_add_batch.clicked.connect(self.show_purchasing_screen)
        self.btn_add_batch.setStyleSheet("background-color: #495057; color: white;") 
        self.btn_refresh_master.clicked.connect(self.load_product_master)
        self.btn_refresh_master.setStyleSheet("background-color: #6C757D; color: white;") 
        self.btn_delete_product.clicked.connect(self.delete_selected_product)
        self.btn_delete_product.setProperty("class", "RedButton") 

        self.control_layout.addWidget(self.btn_add_product)
        self.control_layout.addWidget(self.btn_add_batch)
        self.control_layout.addWidget(self.btn_refresh_master)
        self.control_layout.addWidget(self.btn_delete_product)
        
        # --- 2. Search & Filter Bar ---
        self.filter_search_widget = QWidget()
        filter_search_hlayout = QHBoxLayout(self.filter_search_widget)
        filter_search_hlayout.setContentsMargins(0, 0, 0, 0)  
        
        self.stock_filter_combo = QComboBox()
        self.stock_filter_combo.addItem("In Stock (Qty > 0)", "IN_STOCK")
        self.stock_filter_combo.addItem("Out of Stock (Qty = 0)", "OUT_OF_STOCK")
        self.stock_filter_combo.addItem("All Products", "ALL")
        self.stock_filter_combo.setCurrentText("In Stock (Qty > 0)") 
        self.stock_filter_combo.currentIndexChanged.connect(self.load_product_master)
        self.stock_filter_combo.setFixedWidth(200)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search product name, unit type, or company...")
        self.search_bar.textChanged.connect(self.load_product_master)

        filter_search_hlayout.addWidget(QLabel("View:"))
        filter_search_hlayout.addWidget(self.stock_filter_combo)
        filter_search_hlayout.addWidget(self.search_bar)
        
        # --- 3. Master List & Table ---
        self.master_label = QLabel("Product Master List (Total Stock in Packs) - Double-click for batch details/pricing")
        self.master_label.setStyleSheet("font-weight: bold; font-size: 12pt; margin-top: 10px;")
        
        self.product_master_table = QTableWidget()
        self.product_master_table.setColumnCount(7) # Reduced column count
        self.product_master_table.setHorizontalHeaderLabels(["ID", "Name", "Class", "Company", "Total Stock", "Units/Pack", "Reorder"])
        
        self.product_master_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.product_master_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.product_master_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.product_master_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.product_master_table.doubleClicked.connect(self.show_product_details)
        self.product_master_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Add all permanent elements to the content layout with stretch factors
        self.content_layout.addWidget(self.control_buttons_container, 0)
        self.content_layout.addWidget(self.filter_search_widget, 0)  
        self.content_layout.addWidget(self.master_label, 0)
        
        # Give the main table a high stretch factor (e.g., 10) so it dominates vertical space
        self.content_layout.addWidget(self.product_master_table, 10) 


    def load_product_master(self):
        """Loads product master data, applying stock and text filters."""
        search_text = self.search_bar.text().strip()
        stock_filter = self.stock_filter_combo.currentData()
        
        # 1. Base Query to calculate total stock for all products (active stock only)
        # MODIFIED: Removed p.supplier from SELECT
        base_query = """
        SELECT  
            p.product_id, 
            p.name, 
            c.name, 
            COALESCE(SUM(b.stock_quantity), 0.0) AS TotalStockPacks, 
            p.units_per_pack, 
            p.unit_type, 
            p.reorder_point,
            p.company
        FROM products p
        LEFT JOIN classes c ON p.class_id = c.class_id
        LEFT JOIN stock_batches b ON p.product_id = b.product_id AND b.expiry_date >= STRFTIME('%Y-%m', 'now')
        GROUP BY p.product_id
        """
        
        # 2. Build the WHERE clause (Supplier filtering removed)
        where_clauses = []
        params = []
        
        if search_text:
            search_param = f'%{search_text}%'
            where_clauses.append("(p.name LIKE ? OR c.name LIKE ? OR p.unit_type LIKE ? OR p.company LIKE ?)")
            params.extend([search_param, search_param, search_param, search_param])

        if stock_filter == "IN_STOCK":
            where_clauses.append("TotalStockPacks > 0.001") 
        elif stock_filter == "OUT_OF_STOCK":
            where_clauses.append("TotalStockPacks <= 0.001")

        if where_clauses:
            filter_sql = " HAVING " + " AND ".join(where_clauses)
            final_query = base_query + filter_sql + " ORDER BY p.name ASC"
        else:
            final_query = base_query + " ORDER BY p.name ASC"

        self.db.cursor.execute(final_query, params)
        products = self.db.cursor.fetchall()
        
        self.product_master_table.setRowCount(len(products))
        
        # Set new headers (Supplier column removed)
        self.product_master_table.setColumnCount(7) 
        self.product_master_table.setHorizontalHeaderLabels(["ID", "Name", "Class", "Company", "Total Stock", "Units/Pack", "Reorder"])
        
        for row_num, product in enumerate(products):
            # UPDATED unpacking: p.supplier removed, p.company remains
            product_id, name, class_name, total_stock_packs, units_per_pack, unit_type, reorder_point, company = product
            
            if unit_type in ['TABLET', 'CAPSULE']:
                pack_unit_display = 'Strips'
            elif unit_type in ['SYRUP', 'DROP', 'VIAL', 'INJECTIBLE', 'SPRAY', 'POWDER', 'OINTMENT']:
                pack_unit_display = unit_type.capitalize() + 's' 
            else:
                pack_unit_display = 'Packs'
                
            total_stock_display = f"{total_stock_packs:.2f} {pack_unit_display}"
            
            if total_stock_packs <= reorder_point:
                color = QColor(255, 200, 200) 
            else:
                color = QColor(255, 255, 255) 

            # UPDATED data list: Supplier removed
            data = [
                str(product_id), name, class_name, company or 'N/A', total_stock_display, str(units_per_pack), 
                str(reorder_point)
            ]

            for col in range(len(data)):
                item = QTableWidgetItem(data[col])
                item.setBackground(color)
                self.product_master_table.setItem(row_num, col, item)
        
        self.product_master_table.resizeColumnsToContents()
        
    def show_purchasing_screen(self):
        """Redirects to the main Purchasing tab in the MainWindow."""
        parent_window = self.window()
        if isinstance(parent_window, MainWindow):
            parent_window.show_purchasing_screen()

    def show_product_details(self):
        """Opens the ProductDetailDialog on double-click."""
        selected_rows = self.product_master_table.selectedItems()
        if not selected_rows: return
            
        row_index = selected_rows[0].row()
        product_id = int(self.product_master_table.item(row_index, 0).text())
        
        dialog = ProductDetailDialog(self.db, product_id, self)
        dialog.exec()
        
        self.load_product_master()

    def delete_selected_product(self):
        """Deletes the selected product from the master table after confirmation."""
        selected_rows = self.product_master_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Deletion Error", "Please select a product from the Master List to delete.")
            return

        row_index = selected_rows[0].row()
        product_id_item = self.product_master_table.item(row_index, 0)
        product_name_item = self.product_master_table.item(row_index, 1)

        product_id = int(product_id_item.text())
        product_name = product_name_item.text()

        # Check for existing sales or returns (FK constraint violation)
        self.db.cursor.execute("SELECT COUNT(*) FROM sale_items WHERE product_id = ?", (product_id,))
        sale_count = self.db.cursor.fetchone()[0]
        self.db.cursor.execute("SELECT COUNT(*) FROM returns WHERE product_id = ?", (product_id,))
        return_count = self.db.cursor.fetchone()[0]
        
        if sale_count > 0 or return_count > 0:
            QMessageBox.critical(self, "Deletion Forbidden", f"Product '{product_name}' cannot be deleted. It has recorded sales ({sale_count}) or returns ({return_count}) and must be kept for audit.")
            return

        # Check for active batches (missing check)
        self.db.cursor.execute("SELECT COUNT(*) FROM stock_batches WHERE product_id = ?", (product_id,))
        batch_count = self.db.cursor.fetchone()[0]
        
        # 1. First Confirmation (Standard Warning)
        reply = QMessageBox.question(self, 'Confirm Delete',
            f"Are you SURE you want to delete the product: {product_name}? \n\nTHIS WILL ALSO DELETE ALL ASSOCIATED STOCK BATCHES AND IS IRREVERSIBLE.", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.No:
            return

        # 2. Second Confirmation (Active Stock Warning) - NEW
        if batch_count > 0:
            reply = QMessageBox.warning(self, 'Active Stock Warning',
                        f"WARNING: This product currently has {batch_count} active stock batches. Deleting the product will PERMANENTLY REMOVE all of this stock data (since there is no sales history).\n\nDo you wish to proceed?", 
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return

        # --- Proceed with Deletion ---
        try:
            with self.db.conn:
                # Delete related items and batches
                self.db.cursor.execute("""
                    DELETE FROM purchase_items 
                    WHERE product_id = ? AND p_item_id IN (SELECT purchase_item_id FROM stock_batches WHERE product_id = ?)
                """, (product_id, product_id))
                
                self.db.cursor.execute("DELETE FROM stock_batches WHERE product_id = ?", (product_id,))
                
                # Delete the master product
                self.db.cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
            
            # NEW: Log the Product Deletion event
            user_info = self.db.cursor.execute("SELECT username FROM users WHERE id=?", (self.window().user_id,)).fetchone()
            username = user_info[0] if user_info else 'System'
            self.db.log_action(
                self.window().user_id,
                username,
                'PRODUCT_DELETE',
                product_id,
                f"Permanently deleted product: {product_name}"
            )
            
            QMessageBox.information(self, "Success", f"Product '{product_name}' and all its batches have been deleted.")
            
            self.load_product_master()

        except Exception as e:
            QMessageBox.critical(self, "Deletion Failed", f"Could not delete product: {e}")

    def show_add_product_dialog(self):
        dialog = AddProductDialog(self.db, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_product_master()


# ==============================================================================
# 6.5. NEW CUSTOMER RETURNS WIDGET (INSERT THIS NEW CLASS)
# ==============================================================================




class CustomerReturnsWidget(QWidget):
    """
    Processes customer returns one product at a time by validating the item against
    a specific invoice ID and restoring stock directly.
    """
    
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setLayout(QVBoxLayout())
        self._setup_autocompleter()
        self._setup_ui()
        
    def _setup_autocompleter(self):
        # Product Completer is needed for fast entry
        product_names = self.db.get_product_names()
        self.completer_model = QStringListModel(product_names)
        self.completer = QCompleter(self.completer_model)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)

    def _setup_ui(self):
        title_label = QLabel("Customer Sales Return (One Item at a Time)")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #C82333; margin-bottom: 10px;")
        self.layout().addWidget(title_label)
        
        # --- Input Group ---
        input_group = QGroupBox("Enter Item Details for Return")
        input_layout = QGridLayout(input_group)
        
        self.invoice_input = QLineEdit()
        self.invoice_input.setPlaceholderText("Original Invoice/Sale ID")
        self.invoice_input.setValidator(QIntValidator(1, 999999))
        
        self.product_name_input = QLineEdit()
        self.product_name_input.setPlaceholderText("Product Name that was sold")
        self.product_name_input.setCompleter(self.completer)
        
        self.qty_input = QLineEdit()
        self.qty_input.setPlaceholderText("Quantity to Return (in Base Units, e.g., Tablets)")
        self.qty_input.setValidator(QDoubleValidator(0.01, 99999.99, 2))
        
        self.reason_input = QLineEdit("Customer Requested Refund/Exchange")
        
        input_layout.addWidget(QLabel("Invoice/Sale ID:"), 0, 0); input_layout.addWidget(self.invoice_input, 0, 1)
        input_layout.addWidget(QLabel("Product Name:"), 1, 0); input_layout.addWidget(self.product_name_input, 1, 1)
        input_layout.addWidget(QLabel("Return Quantity:"), 2, 0); input_layout.addWidget(self.qty_input, 2, 1)
        input_layout.addWidget(QLabel("Reason:"), 3, 0); input_layout.addWidget(self.reason_input, 3, 1)
        
        self.process_button = QPushButton("Process Single Item Return")
        self.process_button.setStyleSheet("padding: 15px; font-size: 14pt; background-color: #C82333; color: white;")
        self.process_button.clicked.connect(self.process_single_return)
        
        input_layout.addWidget(self.process_button, 4, 0, 1, 2)
        self.layout().addWidget(input_group)
        
        # --- Result Group ---
        result_group = QGroupBox("Return Result")
        result_layout = QVBoxLayout(result_group)
        
        self.result_label = QLabel("Ready to process returns.")
        self.result_label.setStyleSheet("font-weight: bold; font-size: 11pt; color: #343A40; margin-top: 5px;")
        result_layout.addWidget(self.result_label)
        
        self.layout().addWidget(result_group)
        self.layout().addStretch(1)

    def process_single_return(self):
        """Processes one item return by calling the DB manager directly, after checking invoice status."""
        try:
            sale_id = int(self.invoice_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid numeric Invoice/Sale ID.")
            self.invoice_input.setFocus()
            return

        # --- CRITICAL FIX START: Check Invoice Status ---
        self.db.cursor.execute("SELECT status FROM sales WHERE id = ?", (sale_id,))
        sale_status_row = self.db.cursor.fetchone()
        
        if not sale_status_row:
            QMessageBox.critical(self, "Invalid Invoice", f"Invoice ID {sale_id} not found in sales records.")
            return

        invoice_status = sale_status_row[0]
        if invoice_status == 'Voided':
            QMessageBox.critical(self, "Action Forbidden 🚫", 
                                 f"Invoice ID {sale_id} is already marked as VOIDED. "
                                 "Stock has been restored via the void process. No further returns are permitted.")
            self.invoice_input.clear()
            self.product_name_input.clear()
            self.qty_input.clear()
            return
        # --- CRITICAL FIX END ---

        product_name = self.product_name_input.text().strip()
        
        try:
            qty_to_return = float(self.qty_input.text().strip())
            if qty_to_return <= 0: raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Quantity to return must be a positive number.")
            self.qty_input.setFocus()
            return
            
        reason = self.reason_input.text().strip()
        
        # --- Core Database Call (Remains the same as previous correction) ---
        refund_value, message = self.db.record_sales_return_and_restore_stock(
            sale_id,
            product_name,
            qty_to_return,
            reason,
            self.user_id
        )
        # --------------------------
        
        if refund_value is not None:
            QMessageBox.information(self, "Return Success", 
                                    f"✅ Return of {qty_to_return:.2f} units of {product_name} processed.\n"
                                    f"Stock has been restored and Total Refund/Credit calculated: **${refund_value:.2f}**")
            
            self.result_label.setText(f"Last Return: Invoice {sale_id} | Product: {product_name} | Refund: ${refund_value:.2f}")
            
            # Reset UI for next return
            self.product_name_input.clear()
            self.qty_input.clear()
            self.product_name_input.setFocus()
            
            # Trigger dashboard refresh
            main_window = self.window()
            if isinstance(main_window, MainWindow):
                main_window._check_all_alerts()
                main_window.show_dashboard_screen()
        else:
            QMessageBox.critical(self, "Return Failed", f"❌ Failed to process return: {message}")
            self.result_label.setText(f"FAILURE: {message}")

# --- You must also delete/replace the following related classes from your code base ---
# 1. SelectItemsForReturnDialog 
# 2. ReturnTransactionDetailDialog 
# -------------------------------------------------------------------------------------

class AlertsAndReturnsWidget(QTabWidget):
    """Container for all alerts (Expiry, Low Stock) and all Return functions."""
    
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        
        # 1. Alert Widgets - NOTE: These classes must still be defined below.
        self.expired_items_widget = ExpiredItemsWidget(self.db)
        self.near_expiry_alerts_widget = NearExpiryAlertsWidget(self.db)
        self.low_stock_items_widget = LowStockItemsWidget(self.db)
        
        # 2. Return Widgets (Supplier & Customer)
        self.supplier_returns_widget = SupplierReturnsWidget(self.db)
        self.customer_returns_widget = CustomerReturnsWidget(self.db, self.user_id)
        
        # Add Tabs
        self.addTab(self.expired_items_widget, "Expired Stock (Critical)")
        self.addTab(self.near_expiry_alerts_widget, "Near Expiry Alerts")
        self.addTab(self.low_stock_items_widget, "Low Stock Items")
        self.addTab(self.supplier_returns_widget, "Supplier Returns (Credit)")
        self.addTab(self.customer_returns_widget, "Customer Returns (Refund)") 
        
        self.currentChanged.connect(self._handle_tab_change)
        
    def _handle_tab_change(self, index):
        """Force a reload on alerts/suppliers when their tab is clicked to ensure data is current."""
        tab_widget = self.widget(index)
        if hasattr(tab_widget, 'load_expired_items'):
            tab_widget.load_expired_items()
        elif hasattr(tab_widget, 'load_expiry_alerts'):
            tab_widget.load_expiry_alerts()
        elif hasattr(tab_widget, 'load_low_stock_items'):
            tab_widget.load_low_stock_items()
        elif hasattr(tab_widget, 'load_returnable_batches'):
            tab_widget.load_returnable_batches()

class ExpiredItemsWidget(QWidget):
    # ... (Omitted)
    def __init__(self, db):
        super().__init__()
        self.db = db
        layout = QVBoxLayout(self)
        self.setWindowTitle("Expired Stock")
        
        self.title_label = QLabel("CRITICAL: Expired Batches in Stock (Must be Disposed)")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 12pt; color: #C82333;")
        layout.addWidget(self.title_label)

        self.expired_table = QTableWidget()
        self.expired_table.setColumnCount(6) # Increased column count
        self.expired_table.setHorizontalHeaderLabels(["Product Name", "Batch No.", "Received Date", "Packs", "Units", "Expiry (M/Y)"])
        self.expired_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.expired_table)

        self.refresh_button = QPushButton("Refresh Expired List")
        self.refresh_button.clicked.connect(self.load_expired_items)
        self.refresh_button.setProperty("class", "RedButton")
        layout.addWidget(self.refresh_button)
        
        self.load_expired_items()

    def load_expired_items(self):
        items = self.db.get_expired_batches()
        self.expired_table.setRowCount(len(items))
        
        for row, item in enumerate(items):
            color = QColor(255, 200, 200) # Light red background
            
            data = [
                item['name'], 
                item['batch_number'], # NEW
                item['date_received'], 
                f"{item['pack_qty']:.2f} {item['pack_unit']}", 
                f"{item['base_unit_qty']} {item['base_unit_display']}", 
                item['expiry_date'] # YYYY-MM
            ]
            
            for col in range(len(data)):
                q_item = QTableWidgetItem(data[col])
                q_item.setBackground(color)
                self.expired_table.setItem(row, col, q_item)
                
        self.expired_table.resizeColumnsToContents()
        self.expired_table.resizeRowsToContents()

class NearExpiryAlertsWidget(QWidget):
    # ... (Omitted)
    def __init__(self, db):
        super().__init__()
        self.db = db
        layout = QVBoxLayout(self)
        self.setWindowTitle("Near Expiry Alerts (Next 60 Days)")
        
        self.title_label = QLabel("WARNING: Stock Expiring in Next 60 Days (FEFO Prioritization)")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 12pt; color: #495057;") # Gray Accent
        layout.addWidget(self.title_label)

        self.expiry_table = QTableWidget()
        self.expiry_table.setColumnCount(6) # Increased column count
        self.expiry_table.setHorizontalHeaderLabels(["Status", "Product Name", "Batch No.", "Received Date", "Quantity", "Expiry (M/Y)"])
        self.expiry_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.expiry_table)

        self.refresh_expiry_button = QPushButton("Refresh Near Expiry Alerts")
        self.refresh_expiry_button.clicked.connect(self.load_expiry_alerts)
        self.refresh_expiry_button.setProperty("class", "OrangeButton") # Gray Accent
        layout.addWidget(self.refresh_expiry_button)
        
        self.load_expiry_alerts()

    def load_expiry_alerts(self):
        alerts = self.db.get_expiry_alerts()
        
        alert_categories = [
            ('1_month', QColor(255, 230, 190), "1 MONTH"),         
            ('2_month', QColor(240, 240, 240), "2 MONTHS")      
        ]
        
        # Combine all non-expired alerts for display
        all_alerts = [ (status_key, item) for status_key, _, _ in alert_categories for item in alerts[status_key] ]
        self.expiry_table.setRowCount(len(all_alerts))
        
        for row, (status_key, item_str) in enumerate(all_alerts):
            color = next(c for k, c, t in alert_categories if k == status_key)
            status_text = next(t for k, c, t in alert_categories if k == status_key)
            
            # Example: "Paracetamol (Batch: 1234, Received: 2024-01-01) - Stock: 0.50 strips (5 tabs), Expires: 2025-11"
            try:
                # Part 1: Product Name, Batch, Received Date
                name_batch_date, stock_expiry = item_str.split(' - Stock: ')
                
                # Extract Batch Number and Received Date
                # Finds " (Batch: ...)" and removes it to isolate the product name
                batch_received_part = name_batch_date[name_batch_date.find('(Batch:'):]
                name = name_batch_date[:name_batch_date.find('(Batch:')].strip()

                batch_number = batch_received_part.split('Batch: ')[1].split(', Received:')[0].strip()
                date_received = batch_received_part.split('Received: ')[1].split(')')[0].strip()
                
                # Part 2: Stock and Expiry
                qty_and_units = stock_expiry.split(', Expires: ')[0]
                expiry_date = stock_expiry.split(', Expires: ')[1]

            except Exception: 
                name, batch_number, date_received, qty_and_units, expiry_date = ("N/A", "N/A", "N/A", "N/A", "N/A")

            data = [status_text, name, batch_number, date_received, qty_and_units, expiry_date]
            
            for col in range(6):
                item = QTableWidgetItem(data[col])
                item.setBackground(color)
                self.expiry_table.setItem(row, col, item)
        
        self.expiry_table.resizeColumnsToContents()
        self.expiry_table.resizeRowsToContents()

# ==============================================================================
# 6. ALERT WIDGETS - MODIFIED LowStockItemsWidget
# ==============================================================================

class LowStockItemsWidget(QWidget):
    """
    Shows items below the reorder point.
    MODIFIED: Added a temporary 'Ordered' list functionality using checkboxes.
    """
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.main_layout = QVBoxLayout(self)
        self.setWindowTitle("Low Stock Items")
        
        # New: List to store items marked as ordered
        self.ordered_items_list = [] 
        
        self._setup_ui()
        self.load_low_stock_items()

    def _setup_ui(self):
        
        # --- TOP SECTION: Low Stock List ---
        self.title_label = QLabel("ATTENTION: Items Below Reorder Point (Needs Ordering)")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 12pt; color: #6C757D;")
        self.main_layout.addWidget(self.title_label)

        self.low_stock_table = QTableWidget()
        # FIX: Set column count to 7 (for columns 0 through 6)
        self.low_stock_table.setColumnCount(7)
        self.low_stock_table.setHorizontalHeaderLabels(["Order?", "Product Name", "Current Stock (Packs)", "Unit Type", "Reorder Point", "Supplier", ""])
        
        self.low_stock_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.low_stock_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.low_stock_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Hide the ID column
        self.low_stock_table.setColumnHidden(6, True)
        
        self.main_layout.addWidget(self.low_stock_table)

        # --- Button Controls for Stock Movement ---
        control_hlayout = QHBoxLayout()
        
        self.refresh_button = QPushButton("Refresh Low Stock List")
        self.refresh_button.clicked.connect(self.load_low_stock_items)
        self.refresh_button.setProperty("class", "BlueButton") 
        
        self.mark_ordered_button = QPushButton("Mark Selected as Ordered (Move Down)")
        self.mark_ordered_button.clicked.connect(self.mark_selected_as_ordered)
        self.mark_ordered_button.setStyleSheet("background-color: #008080; color: white;") # Primary Teal
        
        control_hlayout.addWidget(self.refresh_button)
        control_hlayout.addWidget(self.mark_ordered_button)
        self.main_layout.addLayout(control_hlayout)
        
        # --- BOTTOM SECTION: Ordered List ---
        self.main_layout.addSpacing(20)
        self.ordered_summary_label = QLabel("2. Ordered List: 0 Items Selected for Ordering")
        self.ordered_summary_label.setStyleSheet("font-weight: bold; font-size: 12pt; color: #495057;")
        self.main_layout.addWidget(self.ordered_summary_label)

        self.ordered_table = QTableWidget()
        self.ordered_table.setColumnCount(5)
        self.ordered_table.setHorizontalHeaderLabels(["Product Name", "Current Stock", "Reorder Point", "Unit Type", "Supplier"])
        self.ordered_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.ordered_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.main_layout.addWidget(self.ordered_table)

        self.clear_ordered_button = QPushButton("Clear Ordered List / Restore to Low Stock View")
        self.clear_ordered_button.clicked.connect(self.clear_ordered_list)
        self.clear_ordered_button.setProperty("class", "RedButton")
        self.main_layout.addWidget(self.clear_ordered_button)
        
        self.main_layout.addStretch(1)

    def load_low_stock_items(self):
        """Loads data from the DB, then filters out any items already marked as ordered."""
        
        # 1. Fetch all low stock items from DB
        query = """
        WITH CurrentStock AS (
            SELECT product_id, SUM(stock_quantity) AS TotalStock
            FROM stock_batches
            WHERE expiry_date >= STRFTIME('%Y-%m', 'now')
            GROUP BY product_id
        )
        SELECT 
            p.product_id,
            p.name, 
            COALESCE(cs.TotalStock, 0.0), 
            p.reorder_point,
            p.unit_type,
            p.supplier
        FROM products p
        LEFT JOIN CurrentStock cs ON p.product_id = cs.product_id
        WHERE COALESCE(cs.TotalStock, 0.0) <= p.reorder_point
        ORDER BY p.name ASC
        """
        self.db.cursor.execute(query)
        raw_results = self.db.cursor.fetchall()

        # 2. Filter out items already in the ordered list
        ordered_ids = {item['product_id'] for item in self.ordered_items_list}
        filtered_results = [
            r for r in raw_results if r[0] not in ordered_ids
        ]

        self.low_stock_table.setRowCount(len(filtered_results))
        
        for row_num, (product_id, name, stock, reorder, unit_type, supplier) in enumerate(filtered_results):
            color = QColor(255, 255, 200) # Yellow-ish alert background
            
            if unit_type in ['TABLET', 'CAPSULE']:
                pack_unit_display = 'Strips'
            else:
                pack_unit_display = unit_type.capitalize() + 's' if unit_type not in ['SYRUP', 'OINTMENT', 'MISCELLANEOUS'] else unit_type.capitalize()
            
            data = [
                name,
                f"{stock:.2f} {pack_unit_display}",
                unit_type,
                f"{reorder:.2f} {pack_unit_display}",
                supplier
            ]
            
            # --- Column 0: Checkbox ---
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            checkbox_item.setCheckState(Qt.CheckState.Unchecked)
            self.low_stock_table.setItem(row_num, 0, checkbox_item)
            
            # Store ID in the hidden item at index 6
            id_item = QTableWidgetItem(str(product_id))
            self.low_stock_table.setItem(row_num, 6, id_item) # Column 6 stores ProductID
            
            # --- Columns 1-5: Data ---
            for col, value in enumerate(data):
                q_item = QTableWidgetItem(value)
                q_item.setBackground(color)
                # Data columns start at index 1
                self.low_stock_table.setItem(row_num, col + 1, q_item)
                
        self.low_stock_table.resizeColumnsToContents()
        self.low_stock_table.resizeRowsToContents()
        self.update_ordered_table() # Ensure the bottom table is also updated

    def mark_selected_as_ordered(self):
        """Moves checked items from the top table to the temporary ordered list."""
        items_to_move = []

        # 1. Collect all checked rows and retrieve their hidden data
        for row in range(self.low_stock_table.rowCount()):
            checkbox_item = self.low_stock_table.item(row, 0)
            
            # Use safe checks for non-existent items
            if checkbox_item and checkbox_item.checkState() == Qt.CheckState.Checked:
                # FIX: Access item at index 6 directly. It is guaranteed to exist now.
                id_item = self.low_stock_table.item(row, 6) 
                
                if id_item is None:
                    # Should not happen with the column count fix, but defensive programming
                    print(f"Error: Product ID item at row {row}, col 6 is None.")
                    continue
                    
                product_id = int(id_item.text())
                
                # Reconstruct the necessary item dictionary
                item_data = {
                    'product_id': product_id,
                    # Text columns are at indices 1 through 5
                    'name': self.low_stock_table.item(row, 1).text(),
                    'stock': self.low_stock_table.item(row, 2).text(),
                    'unit_type': self.low_stock_table.item(row, 3).text(),
                    'reorder': self.low_stock_table.item(row, 4).text(),
                    'supplier': self.low_stock_table.item(row, 5).text(),
                }
                items_to_move.append(item_data)
        
        # 2. Add collected items to the permanent list
        if not items_to_move:
            QMessageBox.information(self, "Selection Required", "Please select items using the checkboxes to mark them as ordered.")
            return
            
        self.ordered_items_list.extend(items_to_move)

        # 3. Reload the top table (which implicitly removes them via filtering)
        self.load_low_stock_items() 
        
        # 4. Update the bottom table
        self.update_ordered_table()
        
        QMessageBox.information(self, "Action Complete", f"Successfully moved {len(items_to_move)} item(s) to the Ordered List.")


    def update_ordered_table(self):
        """Updates the display of the ordered list table."""
        self.ordered_table.setRowCount(len(self.ordered_items_list))
        
        total_count = len(self.ordered_items_list)
        self.ordered_summary_label.setText(f"2. Ordered List: {total_count} Items Ready for Ordering")
        
        for row_num, item in enumerate(self.ordered_items_list):
            data = [
                item['name'], item['stock'], item['reorder'], item['unit_type'], item['supplier']
            ]
            
            for col, value in enumerate(data):
                q_item = QTableWidgetItem(value)
                q_item.setBackground(QColor(200, 255, 255)) # Light Cyan/Teal background for ordered status
                self.ordered_table.setItem(row_num, col, q_item)
                
        self.ordered_table.resizeColumnsToContents()
        self.ordered_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)


    def clear_ordered_list(self):
        """Clears the ordered list and refreshes the low stock view."""
        if not self.ordered_items_list: return
        
        reply = QMessageBox.question(self, 'Confirm Clear',
            f"Are you sure you want to clear the Ordered List (revert {len(self.ordered_items_list)} item(s) back to the Low Stock View)?\n\nThis does NOT affect database data, only the visual queue.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
        if reply == QMessageBox.StandardButton.Yes:
            self.ordered_items_list = []
            self.load_low_stock_items()
            self.update_ordered_table()
            QMessageBox.information(self, "List Cleared", "Ordered List cleared and Low Stock view refreshed.")


class SupplierReturnsWidget(QWidget):
    """Manages processing of returns for expired/near-expiry stock to suppliers."""

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setLayout(QVBoxLayout())
        self.pending_returns = []
        self.live_batches_data = []  
        self.is_showing_all_stock = False 
        
        self._setup_ui()
        self.load_returnable_batches() 

    # --- UI Setup (Added Search Bar) ---
    def _setup_ui(self):
        # Title and Instructions
        title_label = QLabel("Supplier Returns Management")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #495057; margin-bottom: 10px;")
        self.layout().addWidget(title_label)
        
        self.info_label = QLabel("Showing **Expired/Near Expiry (90 days)** stock for returns. Use the toggle below to view ALL stock.")
        self.info_label.setWordWrap(True)
        self.layout().addWidget(self.info_label)

        # --- Top Panel: Available Batches ---
        self.batches_group = QGroupBox("1. Available Batches for Return")
        batches_layout = QVBoxLayout(self.batches_group)
        
        # NEW: Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter current stock list by Product Name, Supplier, or Batch No...")
        self.search_input.textChanged.connect(self.filter_available_batches)
        batches_layout.addWidget(self.search_input) # Place search bar above the table
        
        self.available_batches_table = QTableWidget()
        self.available_batches_table.setColumnCount(9) 
        self.available_batches_table.setHorizontalHeaderLabels(["Batch ID", "Product", "Supplier Name", "Batch No.", "Expiry (M/Y)", "Qty (Packs)", "Pack Cost ($)", "Units/Pack", "Unit Type"])
        
        self.available_batches_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.available_batches_table.setColumnHidden(0, True) 
        self.available_batches_table.setColumnHidden(7, True) 
        self.available_batches_table.setColumnHidden(8, True) 
        self.available_batches_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.available_batches_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.available_batches_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        batches_layout.addWidget(self.available_batches_table)
        
        # Action Buttons for Top Panel
        action_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh List")
        self.refresh_button.clicked.connect(self.load_returnable_batches)
        self.refresh_button.setProperty("class", "BlueButton")
        
        self.btn_toggle_stock_view = QPushButton("Toggle: Currently Showing OPTIMIZED Stock (Near Expiry)")
        self.btn_toggle_stock_view.setMinimumWidth(250)
        self.btn_toggle_stock_view.clicked.connect(self._toggle_stock_view)
        
        self.qty_to_return_input = QLineEdit("1")
        self.qty_to_return_input.setValidator(QDoubleValidator(0.00, 99999.99, 2))
        self.qty_to_return_input.setFixedWidth(100)
        
        self.add_return_button = QPushButton("Add to Return List")
        self.add_return_button.clicked.connect(self.add_to_pending_returns)
        self.add_return_button.setStyleSheet("background-color: #008080;")
        
        action_layout.addWidget(self.refresh_button)
        action_layout.addWidget(self.btn_toggle_stock_view) 
        action_layout.addStretch(1)
        action_layout.addWidget(QLabel("Packs to Return:"))
        action_layout.addWidget(self.qty_to_return_input)
        action_layout.addWidget(self.add_return_button)
        batches_layout.addLayout(action_layout)
        
        self.layout().addWidget(self.batches_group)
        
        # --- Bottom Panel: Pending Returns (Unchanged) ---
        returns_group = QGroupBox("2. Pending Returns (Will generate a Supplier Credit note)")
        returns_layout = QVBoxLayout(returns_group)
        
        self.pending_returns_table = QTableWidget()
        self.pending_returns_table.setColumnCount(6)
        self.pending_returns_table.setHorizontalHeaderLabels(["Product", "Supplier", "Qty (Packs)", "Pack Cost ($)", "Total Refund ($)", "Linked Order ID"]) 
        self.pending_returns_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.pending_returns_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        returns_layout.addWidget(self.pending_returns_table)
        
        # Finalization
        finalize_layout = QHBoxLayout()
        self.remove_pending_button = QPushButton("Remove Selected")
        self.remove_pending_button.clicked.connect(self.remove_pending_return)
        self.remove_pending_button.setProperty("class", "RedButton")
        
        self.total_refund_label = QLabel("TOTAL REFUND: $0.00")
        self.total_refund_label.setStyleSheet("font-size: 14pt; font-weight: bold; background-color: #E9ECEF; color: #343A40; padding: 5px; border-radius: 4px;")
        
        self.process_button = QPushButton("Process All Returns (Deduct Stock & Credit Supplier)")
        self.process_button.clicked.connect(self.process_all_returns)
        self.process_button.setStyleSheet("padding: 15px; font-size: 16pt; background-color: #495057; color: white;")
        self.process_button.setEnabled(False)
        
        finalize_layout.addWidget(self.remove_pending_button)
        finalize_layout.addWidget(self.total_refund_label)
        finalize_layout.addWidget(self.process_button)
        returns_layout.addLayout(finalize_layout)
        
        self.layout().addWidget(returns_group)
        self.update_pending_returns_table()

    # --- New Toggle Method ---
    def _toggle_stock_view(self):
        """Toggles the state and reloads the stock batches."""
        self.is_showing_all_stock = not self.is_showing_all_stock
        self.load_returnable_batches()

    # --- Search Filter Method (NEW) ---
    def filter_available_batches(self):
        """Filters the displayed batches based on the search input."""
        search_text = self.search_input.text().strip().lower()
        
        # The true source of truth for filtering is the list loaded from the DB
        # This prevents accidental permanent filtering.
        source_data = self._get_uncommitted_live_batches(self._load_raw_batches())
        
        if not search_text:
            self._display_batches(source_data)
            return

        filtered_data = []
        for batch in source_data:
            # Search across Product Name, Supplier, Batch Number, and Expiry Date
            if (search_text in batch['name'].lower() or
                (batch['supplier'] and search_text in batch['supplier'].lower()) or
                (batch['batch_number'] and search_text in batch['batch_number'].lower()) or
                (batch['expiry_date'] and search_text in batch['expiry_date'].lower())):
                filtered_data.append(batch)

        self._display_batches(filtered_data)
        
    # --- Helper to load raw data (NEW, factored out from load_returnable_batches) ---
    def _load_raw_batches(self):
        """Loads raw batch data directly from DB based on current toggle state."""
        
        # --- Query 1: Show ALL Stock ---
        if self.is_showing_all_stock:
            query = """
            SELECT T2.batch_id, T1.product_id, T1.name, T1.supplier, T2.date_received,  
                    T2.expiry_date, T2.stock_quantity, T2.pack_cost_price, T1.units_per_pack, T1.unit_type, T2.batch_number
            FROM products AS T1
            JOIN stock_batches AS T2 ON T1.product_id = T2.product_id
            WHERE T2.stock_quantity > 0  
            ORDER BY T1.supplier ASC, T2.expiry_date ASC;
            """
        # --- Query 2: Show OPTIMIZED (Near Expiry) Stock ---
        else:
            query = """
            SELECT T2.batch_id, T1.product_id, T1.name, T1.supplier, T2.date_received,  
                    T2.expiry_date, T2.stock_quantity, T2.pack_cost_price, T1.units_per_pack, T1.unit_type, T2.batch_number
            FROM products AS T1
            JOIN stock_batches AS T2 ON T1.product_id = T2.product_id
            WHERE T2.stock_quantity > 0 AND T2.expiry_date <= STRFTIME('%Y-%m', 'now', '+90 days')
            ORDER BY T1.supplier ASC, T2.expiry_date ASC;
            """
        
        batches_from_db = self.db.cursor.execute(query).fetchall()
        
        raw_batches = []
        for batch in batches_from_db:
            # Note: Index 7 is now T2.pack_cost_price, not T1.cost_price
            (batch_id, product_id, name, supplier, date_received,
             expiry_date, stock_qty_packs, cost_price, units_per_pack, unit_type, batch_number) = batch
            
            raw_batches.append({
                'batch_id': batch_id, 'product_id': product_id, 'name': name, 'supplier': supplier,  
                'expiry_date': expiry_date, 'stock_qty_packs': stock_qty_packs, 'cost_price': cost_price,  
                'units_per_pack': units_per_pack, 'unit_type': unit_type, 'batch_number': batch_number
            })
        return raw_batches 
       
        
    # --- Helper to apply pending deductions (NEW, factored out) ---
    def _get_uncommitted_live_batches(self, raw_batches):
        """Applies pending returns deductions to the raw batch list."""
        
        temp_live_batches = {b['batch_id']: b.copy() for b in raw_batches}
        
        for pending_item in self.pending_returns:
            batch_id = pending_item['batch_id']
            if batch_id in temp_live_batches:
                temp_live_batches[batch_id]['stock_qty_packs'] -= pending_item['qty_packs']
                temp_live_batches[batch_id]['stock_qty_packs'] = round(temp_live_batches[batch_id]['stock_qty_packs'], 3)
                
                if temp_live_batches[batch_id]['stock_qty_packs'] < 0.001:
                    del temp_live_batches[batch_id]
        
        return list(temp_live_batches.values())


    # --- Modified Loading Method ---
    def load_returnable_batches(self):
        """Fetches all raw data, applies uncommitted deductions, and updates UI state."""
        
        raw_batches = self._load_raw_batches()
        self.live_batches_data = self._get_uncommitted_live_batches(raw_batches)
        
        # Clear existing search/filter
        self.search_input.clear()

        # Update UI text based on state
        if self.is_showing_all_stock:
            self.info_label.setText("Showing **ALL ACTIVE STOCK**.")
            self.batches_group.setTitle("1. Available Batches for Return (ALL STOCK)")
            self.btn_toggle_stock_view.setText("Toggle: Currently Showing ALL Stock")
            self.btn_toggle_stock_view.setStyleSheet("background-color: #C82333; color: white;") 
        else:
            self.info_label.setText("Showing **Expired/Near Expiry (90 days)** stock for returns.")
            self.batches_group.setTitle("1. Available Batches for Return (OPTIMIZED VIEW)")
            self.btn_toggle_stock_view.setText("Toggle: Currently Showing OPTIMIZED Stock (Near Expiry)")
            self.btn_toggle_stock_view.setStyleSheet("background-color: #6C757D; color: white;")
        
        self._display_batches(self.live_batches_data)

    # --- New Display Method (Used by load and filter) ---
    def _display_batches(self, batches_to_display):
        """Populates the table with the given list of batch dicts."""
        self.available_batches_table.setRowCount(len(batches_to_display))
        today_yyyymm = datetime.date.today().strftime('%Y-%m')
        ninety_days_from_now_yyyymm = (datetime.date.today() + datetime.timedelta(days=90)).strftime('%Y-%m')
        
        for row, batch in enumerate(batches_to_display):
            
            stock_qty_packs = batch['stock_qty_packs']
            unit_type = batch['unit_type']
            expiry_date = batch['expiry_date']
            
            pack_unit = 'Strips' if unit_type in ['TABLET', 'CAPSULE'] else unit_type.capitalize() + 's' if unit_type not in ['SYRUP', 'OINTMENT', 'MISCELLANEOUS'] else unit_type.capitalize()
            
            # Determine color
            if expiry_date < today_yyyymm:
                color = QColor(255, 200, 200) # Light red for expired
            elif expiry_date <= ninety_days_from_now_yyyymm:
                color = QColor(255, 255, 200) # Light yellow for near expiry
            else:
                color = QColor(255, 255, 255) # White for normal stock
            
            data = [
                str(batch['batch_id']), batch['name'], batch['supplier'], batch['batch_number'], expiry_date, 
                f"{stock_qty_packs:.2f} {pack_unit}", f"{batch['cost_price']:.2f}",
                str(batch['units_per_pack']), unit_type
            ]
            
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setBackground(color)
                self.available_batches_table.setItem(row, col, item)

        self.available_batches_table.resizeColumnsToContents()
        
    def add_to_pending_returns(self):
        selected_rows = self.available_batches_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Please select a batch from the top table.")
            return

        row_index = selected_rows[0].row()
        
        try:
            qty_to_return = float(self.qty_to_return_input.text() or 0.0)
            if qty_to_return <= 0: raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Quantity to return must be a positive number.")
            return

        # Fetch batch ID from the selected row (which may be filtered)
        batch_id = int(self.available_batches_table.item(row_index, 0).text())
        
        # We need to find the batch data from the FULL live_batches_data list for current stock validation
        live_batch_original = next((b for b in self.live_batches_data if b['batch_id'] == batch_id), None)
        
        if not live_batch_original:
            QMessageBox.critical(self, "Stock Error", "Batch not found/stock already committed. Please refresh.")
            self.load_returnable_batches()
            return
            
        current_stock = live_batch_original['stock_qty_packs'] # Stock is already deducted for pending returns

        if qty_to_return > current_stock + 0.001: 
            QMessageBox.critical(self, "Stock Error", f"Cannot return {qty_to_return:.2f} packs. Only {current_stock:.2f} packs are available in this batch.")
            return

        existing_item = next((item for item in self.pending_returns if item['batch_id'] == batch_id), None)
        today_yyyymm = datetime.date.today().strftime('%Y-%m')
        ninety_days_from_now_yyyymm = (datetime.date.today() + datetime.timedelta(days=90)).strftime('%Y-%m')

        # Dynamically set reason based on expiry status
        if live_batch_original['expiry_date'] < today_yyyymm:
            reason = "Expired Stock"
        elif live_batch_original['expiry_date'] <= ninety_days_from_now_yyyymm:
            reason = "Near Expiry (90 days)"
        else:
            reason = "Quality/Stock Correction" 
        
        if existing_item:
            existing_item['qty_packs'] += qty_to_return
            existing_item['total_refund'] = existing_item['qty_packs'] * live_batch_original['cost_price']
        else:
            order_id = None
            self.db.cursor.execute("""
                SELECT T2.order_id FROM stock_batches AS T1
                JOIN purchase_items AS T2 ON T1.purchase_item_id = T2.p_item_id
                WHERE T1.batch_id = ?
            """, (batch_id,))
            result = self.db.cursor.fetchone()
            if result: order_id = result[0]
            
            self.pending_returns.append({
                'product_id': live_batch_original['product_id'],
                'batch_id': live_batch_original['batch_id'],
                'order_id': order_id, 
                'product_name': live_batch_original['name'],
                'supplier': live_batch_original['supplier'],
                'cost_price': live_batch_original['cost_price'],
                'expiry_date': live_batch_original['expiry_date'],
                'qty_packs': qty_to_return,
                'total_refund': qty_to_return * live_batch_original['cost_price'],
                'reason': reason
            })
        
        # DEDUCT from the live_batches_data list item used for the current view state
        live_batch_original['stock_qty_packs'] -= qty_to_return
        live_batch_original['stock_qty_packs'] = round(live_batch_original['stock_qty_packs'], 3)
        
        # Trigger an update of the displayed table (which will re-apply the filter/toggle logic)
        self.filter_available_batches() 
        self.update_pending_returns_table()
        
        self.qty_to_return_input.setText("1")

    def remove_pending_return(self):
        selected_rows = self.pending_returns_table.selectedItems()
        if not selected_rows: return
        
        row_index = selected_rows[0].row()
        item_to_remove = self.pending_returns.pop(row_index)
        
        removed_qty = item_to_remove['qty_packs']
        batch_id = item_to_remove['batch_id']
        
        # Restore stock to the full master list if possible
        restored = False
        for batch in self.live_batches_data:
            if batch['batch_id'] == batch_id:
                batch['stock_qty_packs'] += removed_qty
                batch['stock_qty_packs'] = round(batch['stock_qty_packs'], 3)
                restored = True
                break
                
        if not restored:
             # Reload the entire list from DB if the item wasn't in our current list (edge case)
            self.load_returnable_batches() 

        self.filter_available_batches() # Re-apply filter/display update
        self.update_pending_returns_table() 

    def update_pending_returns_table(self):
        # ... (unchanged)
        self.pending_returns_table.setRowCount(len(self.pending_returns))
        total_refund_sum = 0.0
        
        for row_num, item in enumerate(self.pending_returns):
            total_refund_sum += item['total_refund']
            
            order_id_display = str(item['order_id']) if item['order_id'] else "N/A"
            
            data = [
                item['product_name'], item['supplier'], f"{item['qty_packs']:.2f}", 
                f"{item['cost_price']:.2f}", f"{item['total_refund']:.2f}", order_id_display
            ]
            
            for col, value in enumerate(data):
                self.pending_returns_table.setItem(row_num, col, QTableWidgetItem(value))
                
        self.total_refund_label.setText(f"TOTAL REFUND: ${total_refund_sum:.2f}")
        self.process_button.setEnabled(len(self.pending_returns) > 0)
        self.pending_returns_table.resizeColumnsToContents()

    def process_all_returns(self):
        # ... (unchanged)
        if not self.pending_returns:
            QMessageBox.warning(self, "Process Error", "No items pending for return.")
            return

        total_refund = sum(item['total_refund'] for item in self.pending_returns)
        
        reply = QMessageBox.question(self, 'Confirm Return Process',
            f"Confirm return of {len(self.pending_returns)} items, totaling **${total_refund:.2f}** in potential refund? \n\nStock will be DEDUCTED and a credit recorded (linked to original order where possible).", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            successful_returns = 0
            items_to_process = list(self.pending_returns)
            
            try:
                for item in items_to_process:
                    success = self.db.record_return_and_deduct_stock(
                        item['product_id'], item['batch_id'], item['qty_packs'],
                        item['cost_price'], item['total_refund'], item['supplier'], item['reason']
                    )
                    
                    if success:
                        successful_returns += 1
                        self.pending_returns.pop(self.pending_returns.index(item)) 
                    else:
                        QMessageBox.critical(self, "Return Failed", f"Failed to process return for {item['product_name']} (Batch {item['batch_id']}). Aborting.")
                        break
            except Exception as e:
                QMessageBox.critical(self, "Database Transaction Error", f"A critical error occurred during return processing: {e}")

            self.update_pending_returns_table()
            self.load_returnable_batches()
            
            if successful_returns > 0:
                main_window = self.window()
                user_info = self.db.cursor.execute("SELECT username FROM users WHERE id=?", (main_window.user_id,)).fetchone()
                username = user_info[0] if user_info else 'System'
                self.db.log_action(
                    main_window.user_id,
                    username,
                    'RETURNS_PROCESSED',
                    None,
                    f"Processed {successful_returns} returns. Total Refund Value: ${total_refund:.2f}"
                )
                
                if isinstance(self.parent().parent(), QMainWindow):
                    self.parent().parent()._check_all_alerts()
                    self.parent().parent().show_dashboard_screen()

# ==============================================================================
# 7. DASHBOARD WIDGET (UNCHANGED)
# ==============================================================================

# ==============================================================================
# NEW: DEDICATED DAILY SALES VIEWER WIDGET
# ==============================================================================

class DailySalesViewerWidget(QWidget):
    """Allows viewing all sales and calculating daily gross profit for a selected date."""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.main_layout = QVBoxLayout(self)
        self.current_report_data = [] # To hold the raw data for filtering
        self._setup_ui()
        self.load_daily_sales()

    def _setup_ui(self):
        title_label = QLabel("Daily Sales & Profit Overview")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #008080; margin-bottom: 10px;")
        self.main_layout.addWidget(title_label)
        
        # --- Controls ---
        controls_hlayout = QHBoxLayout()
        
        self.date_selector = QDateEdit(QDate.currentDate())
        self.date_selector.setCalendarPopup(True)
        self.date_selector.setDisplayFormat("yyyy-MM-dd")
        self.date_selector.dateChanged.connect(self.load_daily_sales)

        self.btn_load_sales = QPushButton("Load Sales for Selected Date")
        self.btn_load_sales.clicked.connect(self.load_daily_sales)
        self.btn_load_sales.setStyleSheet("background-color: #495057; color: white;")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Filter sales by Patient Name, Doctor Ref, or Invoice ID...")
        self.search_bar.textChanged.connect(self._filter_sales_table)

        controls_hlayout.addWidget(QLabel("Select Date:"))
        controls_hlayout.addWidget(self.date_selector)
        controls_hlayout.addWidget(self.btn_load_sales)
        controls_hlayout.addWidget(self.search_bar)
        controls_hlayout.setStretchFactor(self.search_bar, 1)

        self.main_layout.addLayout(controls_hlayout)
        
        # --- Summary Card ---
        self.summary_label = QLabel("Summary: Loading...")
        self.summary_label.setStyleSheet("font-weight: bold; padding: 10px; border: 1px solid #008080; background-color: #E6F5F5; color: #343A40; border-radius: 4px; margin-top: 10px;")
        self.main_layout.addWidget(self.summary_label)

        # --- Table ---
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(7)
        self.sales_table.setHorizontalHeaderLabels([
            "Invoice ID (Dbl-Click)", "Time", "Patient Name", "Doctor Ref",
            "Total Revenue ($)", "Discount ($)", "Gross Profit ($)"
        ])
        self.sales_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.sales_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.sales_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.sales_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.sales_table.doubleClicked.connect(self._handle_table_double_click)
        
        self.main_layout.addWidget(self.sales_table)
        self.main_layout.addStretch(1)

    def load_daily_sales(self):
        """Loads data using the new DB method and updates the table/summary."""
        selected_date = self.date_selector.date().toString("yyyy-MM-dd")
        self.current_report_data = self.db.get_daily_sales_and_profit(selected_date)
        
        daily_total_revenue = sum(s['revenue'] for s in self.current_report_data)
        daily_total_profit = sum(s['profit'] for s in self.current_report_data)
        
        # Update Summary
        self.summary_label.setText(
            f"Summary for **{selected_date}** ({len(self.current_report_data)} Finalized Sales): "
            f"Total Revenue: **₹{daily_total_revenue:.2f}** | "
            f"Total Gross Profit: **₹{daily_total_profit:.2f}**"
        )

        self._populate_sales_table(self.current_report_data)

    def _filter_sales_table(self):
        """Filters the displayed table based on the search bar content."""
        search_text = self.search_bar.text().strip().lower()
        
        if not search_text:
            filtered_data = self.current_report_data
        else:
            filtered_data = [
                sale for sale in self.current_report_data 
                if search_text in str(sale['id']).lower() or
                   search_text in sale['patient'].lower() or
                   search_text in sale['doctor'].lower()
            ]
            
        self._populate_sales_table(filtered_data)


    def _populate_sales_table(self, data):
        """Populates the sales table with the provided data list."""
        self.sales_table.setRowCount(len(data))
        
        for row_num, sale in enumerate(data):
            
            # Use data from the sales dictionary
            sale_id = str(sale['id'])
            profit = sale['profit']
            
            # Apply color if profit is zero or negative
            color = QColor(255, 200, 200) if profit < 0.001 else QColor(255, 255, 255)
            
            data_to_display = [
                sale_id, sale['time'], sale['patient'], sale['doctor'],
                f"{sale['revenue']:.2f}", f"{sale['discount']:.2f}", f"{profit:.2f}"
            ]
            
            for col_num, value in enumerate(data_to_display):
                item = QTableWidgetItem(value)
                item.setBackground(color)
                
                # Align numerical and ID columns right
                if col_num in [0, 4, 5, 6]:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                
                self.sales_table.setItem(row_num, col_num, item)
                
        self.sales_table.resizeColumnsToContents()
        self.sales_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)


    def _handle_table_double_click(self, index):
        """Opens the SaleDetailDialog when a row is double-clicked."""
        try:
            # Check if the click was on a valid row and column (Invoice ID is column 0)
            if self.sales_table.item(index.row(), 0):
                sale_id = int(self.sales_table.item(index.row(), 0).text())
                dialog = SaleDetailDialog(self.db, sale_id, self)
                dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open sale details: {e}")


class DashboardWidget(QWidget):
    # ... (Omitted)
    def __init__(self, db, user_role):
        super().__init__()
        self.db = db
        self.user_role = user_role
        self.setLayout(QVBoxLayout())
        self.load_dashboard()

    def _create_card(self, title, value, style_color="#333", prefix=""):
        card = QWidget()
        card.setProperty("class", "Card")
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setProperty("class", "CardTitle")
        
        # Determine if value is numeric for formatting
        if isinstance(value, (int, float)):
              # Only apply comma separator if it's a number
              value_str = f"{value:,}"
        else:
              # Use the value as is (assumed pre-formatted string for currency)
              value_str = str(value)
              
        value_label = QLabel(f"{prefix}{value_str}")
        value_label.setProperty("class", "CardValue")
        value_label.setStyleSheet(f"color: {style_color};")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        return card

    def load_dashboard(self):
        # Clear existing layout
        while self.layout().count():
            item = self.layout().takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        data = self.db.get_dashboard_data()

        # 1. Header
        welcome_label = QLabel(f"Welcome back, {self.user_role}!")
        welcome_label.setStyleSheet("font-size: 18pt; font-weight: bold; margin-bottom: 15px; color: #008080;") # Primary Teal
        self.layout().addWidget(welcome_label)
        
        # 2. Key Performance Indicators (KPIs)
        kpi_layout = QHBoxLayout()
        
        # Sales Revenue KPI
        kpi_layout.addWidget(self._create_card(
            "7-Day Revenue", f"{data['last_7_days_revenue']:.2f}", prefix="₹", style_color="#008080" # Primary Teal
        ))
        # Transactions KPI
        kpi_layout.addWidget(self._create_card(
            "7-Day Transactions", data['last_7_days_transactions'], style_color="#6C757D" # Secondary Gray
        ))
        # Inventory Value KPI
        kpi_layout.addWidget(self._create_card(
            "Total Inventory Cost Value", f"{data['inventory_value']:.2f}", prefix="₹", style_color="#495057" # Gray Accent
        ))
        
        self.layout().addLayout(kpi_layout)
        
        # 3. Alerts Section
        alerts_label = QLabel("Critical & Stock Alerts")
        alerts_label.setStyleSheet("font-size: 16pt; font-weight: bold; margin-top: 20px; color: #C82333;") # Critical Red
        self.layout().addWidget(alerts_label)

        alert_layout = QHBoxLayout()
        
        # Expired Count Card 
        expired_card = self._create_card("Expired Stock", data['expired_count'], style_color="#C82333") # Critical Red
        alert_layout.addWidget(expired_card)

        # Near Expiry Count Card 
        near_expiry_card = self._create_card("Near Expiry (60 Days)", data['near_expiry_count'], style_color="#495057") # Gray Accent
        alert_layout.addWidget(near_expiry_card)
        
        # Low Stock Count Card 
        low_stock_card = self._create_card("Low Stock Items (Reorder)", data['low_stock_count'], style_color="#343A40") # Dark Gray Text
        alert_layout.addWidget(low_stock_card)

        self.layout().addLayout(alert_layout)
        
        self.layout().addStretch(1)

# ==============================================================================
# 8. MAIN APPLICATION WINDOW (COMPLETE) - MODIFIED FOR NEW NAVIGATION
# ==============================================================================

class MainWindow(QMainWindow):
    def __init__(self, db, user_id, user_role='Admin'):
        super().__init__()
        self.db = db
        self.user_role = user_role
        self.user_id = user_id
        
        self.setWindowTitle(f"Shree Ram Medical Stores (Logged in as {self.user_role})")
        # MODIFIED: Set a minimum size only, deferring to showMaximized for initial window state.
        self.setMinimumSize(1000, 650)
        
        self._create_menu()
        self._create_status_bar()
        self._setup_main_layout()
        
        # --- AUTO-BACKUP CALL ---
        self.run_startup_backup()
        # ------------------------
        
        self._check_all_alerts()
        self.show_dashboard_screen() # Display dashboard on startup
        # NOTE: showMaximized() must be called after initialization in the entry point.

    def run_startup_backup(self):
        """Runs the daily backup and updates the status bar on startup."""
        success, message = self.db.perform_daily_backup()
        if success:
            self.statusBar.showMessage(f"System Ready. Auto-Backup completed successfully.", 5000)
        else:
            self.statusBar.showMessage(f"System Ready. WARNING: Auto-Backup failed. See console for details.", 10000)

    def _create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        backup_action = file_menu.addAction("Database Backup (Manual)")
        backup_action.triggered.connect(self.backup_database)
        file_menu.addAction("Exit").triggered.connect(self.close)

    def _create_status_bar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage(f"System Ready.")
        
    def _setup_main_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        nav_panel = QVBoxLayout()
        nav_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # --- SALES & DASHBOARD ---
        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_dashboard.setObjectName("NavButton")
        self.btn_dashboard.setProperty("class", "BlueButton")
        self.btn_dashboard.clicked.connect(self.show_dashboard_screen)
        
        self.btn_pos = QPushButton("Point of Sale (F1)")
        self.btn_pos.setObjectName("NavButton")
        self.btn_pos.setProperty("class", "TealPrimary")
        self.btn_pos.clicked.connect(self.show_pos_screen)
        
        # --- OPERATIONS & MANAGEMENT (New Grouping) ---
        self.btn_inventory = QPushButton("Inventory Management")
        self.btn_inventory.setObjectName("NavButton")
        self.btn_inventory.setProperty("class", "GraySecondary") 
        self.btn_inventory.clicked.connect(self.show_inventory_screen)
        
        self.btn_reports = QPushButton("Reports & Analytics")
        self.btn_reports.setObjectName("NavButton")
        self.btn_reports.setProperty("class", "OrangeButton")
        self.btn_reports.clicked.connect(self.show_reports_screen)
        
        self.btn_purchasing = QPushButton("Purchasing & Payables")
        self.btn_purchasing.setObjectName("NavButton")
        self.btn_purchasing.setProperty("class", "GrayAccent")
        self.btn_purchasing.clicked.connect(self.show_purchasing_screen)
        
        self.btn_daily_sales = QPushButton("Daily Sales & Profit")
        self.btn_daily_sales.setObjectName("NavButton")
        self.btn_daily_sales.setProperty("class", "TealPrimary")
        self.btn_daily_sales.clicked.connect(self.show_daily_sales_screen)
        
        self.btn_old_bills = QPushButton("Re-Print Old Bills")
        self.btn_old_bills.setObjectName("NavButton")
        self.btn_old_bills.setProperty("class", "GraySecondary")
        self.btn_old_bills.clicked.connect(self.show_old_bills_screen)
        
        # --- RETURNS ---
        self.btn_customer_returns = QPushButton("Customer Returns")
        self.btn_customer_returns.setObjectName("NavButton")
        self.btn_customer_returns.setProperty("class", "RedButton")
        self.btn_customer_returns.clicked.connect(self.show_customer_returns_screen)
        
        self.btn_supplier_returns = QPushButton("Supplier Returns")
        self.btn_supplier_returns.setObjectName("NavButton")
        self.btn_supplier_returns.setProperty("class", "ReturnButton")
        self.btn_supplier_returns.clicked.connect(self.show_supplier_returns_screen)
        
        # --- ALERTS ---
        self.btn_expired = QPushButton("Expired Items")
        self.btn_expired.setObjectName("NavButton")
        self.btn_expired.setProperty("class", "RedButton")
        self.btn_expired.clicked.connect(self.show_expired_screen)
        
        self.btn_near_expiry = QPushButton("Near Expiry Alerts")
        self.btn_near_expiry.setObjectName("NavButton")
        self.btn_near_expiry.setProperty("class", "OrangeButton")
        self.btn_near_expiry.clicked.connect(self.show_near_expiry_screen)

        self.btn_low_stock = QPushButton("Low Stock Items")
        self.btn_low_stock.setObjectName("NavButton")
        self.btn_low_stock.setProperty("class", "BlueButton")
        self.btn_low_stock.clicked.connect(self.show_low_stock_screen)
        
        # --- Apply to Layout ---
        nav_panel.addWidget(self.btn_dashboard) 
        nav_panel.addWidget(self.btn_pos)
        nav_panel.addSpacing(20)
        
        nav_panel.addWidget(QLabel("Operations & Management:"))
        nav_panel.addWidget(self.btn_inventory)
        nav_panel.addWidget(self.btn_reports)
        nav_panel.addWidget(self.btn_purchasing)
        nav_panel.addWidget(self.btn_daily_sales) 
        nav_panel.addWidget(self.btn_old_bills)
        nav_panel.addSpacing(20)
        
        nav_panel.addWidget(QLabel("Returns:"))
        nav_panel.addWidget(self.btn_customer_returns)
        nav_panel.addWidget(self.btn_supplier_returns)
        nav_panel.addSpacing(20)
        
        nav_panel.addWidget(QLabel("Alerts:"))
        nav_panel.addWidget(self.btn_expired)
        nav_panel.addWidget(self.btn_near_expiry)
        nav_panel.addWidget(self.btn_low_stock)


        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        
        # Stretch factors for proper layout balance
        main_layout.addLayout(nav_panel, 1)
        main_layout.addWidget(self.content_widget, 4)

    def _check_all_alerts(self):
        """Checks for alerts and updates status bar (WITHOUT highlighting nav buttons)."""
        alerts = self.db.get_expiry_alerts()
        data = self.db.get_dashboard_data()
        
        expired_count = len(alerts['expired'])
        near_expiry_count = len(alerts['1_month']) + len(alerts['2_month'])
        low_stock_count = data['low_stock_count']
        
        # Reset styles to base QSS defined in properties
        self.btn_expired.setStyleSheet("background-color: #C82333; color: white;")
        self.btn_near_expiry.setStyleSheet("background-color: #495057; color: white;")
        self.btn_low_stock.setStyleSheet("background-color: #6C757D; color: white;")
        self.btn_supplier_returns.setStyleSheet("background-color: #495057; color: white;")
        self.btn_customer_returns.setStyleSheet("background-color: #C82333; color: white;")
        self.btn_old_bills.setStyleSheet("background-color: #6C757D; color: white;") 
        self.btn_daily_sales.setStyleSheet("background-color: #008080; color: white;") 
        
        status_message = f"Logged in as: {self.user_role} | System Ready."
        
        if expired_count > 0:
            status_message = f"CRITICAL: {expired_count} expired batches! Check 'Expired Items'!"

        if near_expiry_count > 0:
            if expired_count == 0: 
                status_message = f"WARNING: {near_expiry_count} batches near expiry. Check 'Near Expiry Alerts'!"
            
        if low_stock_count > 0:
            if expired_count == 0 and near_expiry_count == 0:
                status_message = f"LOW STOCK: {low_stock_count} items need reordering. Check 'Low Stock Items'!"
            
        self.statusBar.showMessage(status_message, 0)

    def backup_database(self):
        """
        Opens a QFileDialog to select a save location and copies the database file 
        to that separate location (Manual Backup).
        """
        default_filename = f"pharmacy_pos_backup_{datetime.date.today().strftime('%Y%m%d')}_manual.db"
        
        file_name, _ = QFileDialog.getSaveFileName(self, 
                                                   "Save Database Backup", 
                                                   default_filename, 
                                                   "SQLite Database Files (*.db);;All Files (*)")

        if file_name:
            try:
                self.db.conn.close() 
                shutil.copyfile(self.db.db_name, file_name)
                self.db.connect() 
                
                QMessageBox.information(self, "Backup Success", f"Database successfully backed up to:\n{file_name}")
            
            except Exception as e:
                self.db.connect()
                QMessageBox.critical(self, "Backup Error", f"Could not create backup: {e}")
        
    def clear_content(self):
        for i in reversed(range(self.content_layout.count())): 
            widget = self.content_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
                
    def show_dashboard_screen(self):
        self.clear_content()
        dashboard_widget = DashboardWidget(self.db, self.user_role)
        self.content_layout.addWidget(dashboard_widget)
        self._check_all_alerts()
        
    def show_pos_screen(self):
        self.clear_content()
        pos_widget = POSWidget(self.db, self.user_id) 
        self.content_layout.addWidget(pos_widget)
        
    def show_inventory_screen(self):
        self.clear_content()
        inventory_widget = InventoryWidget(self.db)
        self.content_layout.addWidget(inventory_widget)
        self._check_all_alerts()

    def show_purchasing_screen(self):
        self.clear_content()
        purchasing_widget = PurchasingWidget(self.db, self.user_id)
        self.content_layout.addWidget(purchasing_widget)
        self._check_all_alerts()

    # --- INDIVIDUAL ALERT SCREENS (Reload on navigation) ---
    def show_expired_screen(self):
        self.clear_content()
        expired_widget = ExpiredItemsWidget(self.db)
        self.content_layout.addWidget(expired_widget)
        self._check_all_alerts()
        
    def show_near_expiry_screen(self):
        self.clear_content()
        near_expiry_widget = NearExpiryAlertsWidget(self.db)
        self.content_layout.addWidget(near_expiry_widget)
        self._check_all_alerts()
        
    def show_low_stock_screen(self): 
        self.clear_content()
        low_stock_widget = LowStockItemsWidget(self.db)
        self.content_layout.addWidget(low_stock_widget)
        self._check_all_alerts()

    def show_supplier_returns_screen(self):
        self.clear_content()
        returns_widget = SupplierReturnsWidget(self.db)
        self.content_layout.addWidget(returns_widget)
        self._check_all_alerts()
        
    # --- RETURNS & OPERATIONS SCREENS ---
    def show_customer_returns_screen(self):
        self.clear_content()
        customer_returns_widget = CustomerReturnsWidget(self.db, self.user_id)
        self.content_layout.addWidget(customer_returns_widget)
        self._check_all_alerts()
        
    def show_old_bills_screen(self):
        self.clear_content()
        old_bill_widget = OldBillViewerWidget(self.db)
        self.content_layout.addWidget(old_bill_widget)
        self._check_all_alerts()
        
    def show_daily_sales_screen(self):
        self.clear_content()
        daily_sales_widget = DailySalesViewerWidget(self.db)
        self.content_layout.addWidget(daily_sales_widget)
        self._check_all_alerts()

    def show_reports_screen(self):
        self.clear_content()
        reports_widget = ReportsWidget(self.db) 
        self.content_layout.addWidget(reports_widget)

    def closeEvent(self, event):
        self.db.close()
        event.accept()


# ==============================================================================
# 9. APPLICATION ENTRY POINT (MODIFIED to use showMaximized)
# ==============================================================================

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS_THEME) 

    db = DatabaseManager()
    
    if not db.conn:
        QMessageBox.critical(None, "Fatal Error", "Database connection failed. Check file permissions or path.")
        sys.exit(1)
        
    default_user_id = db.add_initial_data() 
    
    if default_user_id == 0:
        QMessageBox.critical(None, "Fatal Error", "Initial data setup failed (Admin user not created). Exiting.")
        sys.exit(1)
    
    window = MainWindow(db, default_user_id)
    window.showMaximized() # MODIFIED: Opens the window in maximized state.
    
    sys.exit(app.exec())


    
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS_THEME) 

    db = DatabaseManager()
    
    if not db.conn:
        QMessageBox.critical(None, "Fatal Error", "Database connection failed. Check file permissions or path.")
        sys.exit(1)
        
    default_user_id = db.add_initial_data() 
    
    if default_user_id == 0:
        QMessageBox.critical(None, "Fatal Error", "Initial data setup failed (Admin user not created). Exiting.")
        sys.exit(1)
    
    window = MainWindow(db, default_user_id)
    window.show() 
    
    sys.exit(app.exec())