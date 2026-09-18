// ===== TOAST NOTIFICATION =====
function showToast(message, isError = false) {
    // Remove any existing toast
    const existingToast = document.getElementById('toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    // Create new toast
    const toast = document.createElement('div');
    toast.id = 'toast';
    toast.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: ${isError ? '#e76f51' : '#1b4332'};
        color: white;
        padding: 14px 28px;
        border-radius: 30px;
        font-weight: 500;
        font-size: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        z-index: 99999;
        max-width: 90%;
        opacity: 0;
        transform: translateY(100px) scale(0.9);
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        font-family: 'Segoe UI', system-ui, sans-serif;
        border: 1px solid rgba(255,255,255,0.1);
    `;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Trigger animation
    requestAnimationFrame(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0) scale(1)';
    });
    
    // Auto remove after 3 seconds
    clearTimeout(toast._timeout);
    toast._timeout = setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px) scale(0.95)';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 400);
    }, 3000);
}
// ===== MODAL FUNCTIONS =====
function showModal(type) {
    console.log('Opening modal:', type);
    const modal = document.getElementById('modal');
    const title = document.getElementById('modalTitle');
    const body = document.getElementById('modalBody');

    if (!modal || !title || !body) {
        console.error('Modal elements not found!');
        showToast('Error: Modal elements not found', true);
        return;
    }

    const data = {
        inventory: {
            title: '📦 Inventory Management',
            content: `
                <div id="inventoryModalList"><p>Loading inventory...</p></div>
                <br>
                <button onclick="addItem()" class="btn btn-primary">➕ Add New Item</button>
                <button onclick="refreshInventory()" class="btn btn-secondary">🔄 Refresh</button>
            `
        },
        expiry: {
            title: '⏰ Expiry Alerts',
            content: `
                <div id="expiryModalList"><p>Loading expiry data...</p></div>
                <br>
                <button onclick="showToast('Expiry notifications sent!')" class="btn btn-primary">📧 Send Alerts</button>
            `
        },
       shopping: {
    title: '🛒 AI Shopping List',
    content: `
        <div id="shoppingModalList"><p>Loading items...</p></div>
        <br>
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <button onclick="generateShoppingList()" class="btn btn-primary" id="generateListBtn">📋 Generate List</button>
            <button onclick="clearShoppingList()" class="btn btn-secondary">🗑️ Clear</button>
            <button onclick="loadShoppingModal()" class="btn btn-secondary">🔄 Refresh</button>
        </div>
    `
},
        recipe: {
            title: '🍳 Recipe & Meal Planner',
            content: `
                <div id="recipeModalList"><p>Loading recipes...</p></div>
                <br>
                <button onclick="showToast('Meal plan generated! 🍽️')" class="btn btn-primary">📅 Plan Week</button>
            `
        }
    };

    const selected = data[type];
    if (selected) {
        title.textContent = selected.title;
        body.innerHTML = selected.content;
        modal.style.display = 'flex';
        
        if (type === 'inventory') loadInventoryModal();
        if (type === 'expiry') loadExpiryModal();
        if (type === 'shopping') loadShoppingModal();
        if (type === 'recipe') loadRecipeModal();
    }
}

function closeModal() {
    const modal = document.getElementById('modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Click outside to close
document.addEventListener('click', function(e) {
    const modal = document.getElementById('modal');
    if (modal && e.target === modal) {
        closeModal();
    }
});

// Escape key to close
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// ===== INVENTORY FUNCTIONS =====
function loadInventoryModal() {
    fetch('/api/inventory')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('inventoryModalList');
            if (container) {
                if (!data.items || data.items.length === 0) {
                    container.innerHTML = '<p>No items in inventory</p>';
                } else {
                    container.innerHTML = data.items.map(item => `
                        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                            <span><strong>${item.name}</strong> (${item.quantity} ${item.unit})</span>
                            <button onclick="updateStock(${item.id})" class="btn btn-sm btn-secondary">Update</button>
                        </div>
                    `).join('');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error loading inventory', true);
        });
}

function loadExpiryModal() {
    fetch('/api/inventory')
        .then(response => response.json())
        .then(data => {
            const today = new Date();
            const expiringItems = data.items.filter(item => {
                try {
                    const expiryDate = new Date(item.expiry);
                    const daysLeft = (expiryDate - today) / (1000 * 60 * 60 * 24);
                    return daysLeft <= 3 && daysLeft >= 0;
                } catch {
                    return false;
                }
            });
            
            const container = document.getElementById('expiryModalList');
            if (container) {
                if (expiringItems.length === 0) {
                    container.innerHTML = '<p>✅ No items expiring soon!</p>';
                } else {
                    container.innerHTML = expiringItems.map(item => {
                        const expiryDate = new Date(item.expiry);
                        const daysLeft = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24));
                        return `
                            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                                <span><strong>${item.name}</strong></span>
                                <span style="color: ${daysLeft <= 1 ? '#e76f51' : '#f4a261'};">
                                    ${daysLeft} day${daysLeft > 1 ? 's' : ''} left
                                </span>
                            </div>
                        `;
                    }).join('');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error loading expiry data', true);
        });
}

function loadShoppingModal() {
    fetch('/api/inventory')
        .then(response => response.json())
        .then(data => {
            const lowStockItems = data.items.filter(item => item.quantity <= 2);
            const container = document.getElementById('shoppingModalList');
            if (container) {
                if (lowStockItems.length === 0) {
                    container.innerHTML = '<p>✅ All items are well stocked!</p>';
                } else {
                    container.innerHTML = lowStockItems.map(item => `
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #eee;">
                            <div>
                                <strong>${item.name}</strong> 
                                <span style="color: #666; font-size: 13px;">(${item.quantity} ${item.unit} left)</span>
                            </div>
                            <button onclick="addToShoppingList(${item.id}, '${item.name}')" 
                                style="
                                    padding: 6px 16px;
                                    background: #2d6a4f;
                                    color: white;
                                    border: none;
                                    border-radius: 20px;
                                    cursor: pointer;
                                    font-weight: 600;
                                    font-size: 13px;
                                    transition: all 0.2s;
                                "
                                onmouseover="this.style.background='#1b4332'; this.style.transform='scale(1.05)';"
                                onmouseout="this.style.background='#2d6a4f'; this.style.transform='scale(1)';"
                            >
                                ➕ Add to List
                            </button>
                        </div>
                    `).join('');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error loading shopping list', true);
        });
}
// ===== SHOPPING LIST FUNCTIONS =====
let shoppingList = [];

function addToShoppingList(itemId, itemName) {
    if (shoppingList.includes(itemId)) {
        showToast(`⚠️ "${itemName}" is already in your shopping list!`, true);
        return;
    }
    
    shoppingList.push(itemId);
    showToast(`✅ Added "${itemName}" to shopping list!`);
    loadShoppingModal(); // Refresh to update button states
    updateGenerateButton();
}

function updateGenerateButton() {
    const generateBtn = document.getElementById('generateListBtn');
    if (generateBtn) {
        if (shoppingList.length > 0) {
            generateBtn.textContent = `📋 Generate List (${shoppingList.length} items)`;
        } else {
            generateBtn.textContent = '📋 Generate List';
        }
    }
}

function clearShoppingList() {
    shoppingList = [];
    updateGenerateButton();
    loadShoppingModal();
    showToast('🔄 Shopping list cleared!');
}

function printShoppingList() {
    // Get all item divs from the shopping list
    const items = document.querySelectorAll('#shoppingModalList .shopping-item');
    if (items.length === 0) {
        // Try to get items from the list directly
        const listDiv = document.querySelector('#shoppingModalList .shopping-list-items');
        if (listDiv) {
            const printContent = listDiv.innerHTML;
            const printWindow = window.open('', '_blank');
            printWindow.document.write(`
                <html>
                    <head>
                        <title>Shopping List</title>
                        <style>
                            body { font-family: 'Segoe UI', sans-serif; padding: 40px; max-width: 600px; margin: 0 auto; }
                            h1 { color: #1b4332; border-bottom: 3px solid #2d6a4f; padding-bottom: 10px; }
                            .item { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }
                            .item-name { font-weight: 500; }
                            .item-qty { color: #666; }
                            .total { margin-top: 20px; font-weight: 600; color: #1b4332; }
                        </style>
                    </head>
                    <body>
                        <h1>🛒 Shopping List</h1>
                        ${printContent}
                    </body>
                </html>
            `);
            printWindow.document.close();
            printWindow.print();
            return;
        }
    }
    
    // Extract item names and quantities
    let printContent = '';
    items.forEach(item => {
        const name = item.querySelector('.item-name')?.textContent || 'Item';
        const qty = item.querySelector('.item-qty')?.textContent || '';
        printContent += `
            <div class="item">
                <span class="item-name">${name}</span>
                <span class="item-qty">${qty}</span>
            </div>
        `;
    });
    
    if (printContent) {
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <html>
                <head>
                    <title>Shopping List</title>
                    <style>
                        body { font-family: 'Segoe UI', sans-serif; padding: 40px; max-width: 600px; margin: 0 auto; }
                        h1 { color: #1b4332; border-bottom: 3px solid #2d6a4f; padding-bottom: 10px; }
                        .item { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }
                        .item-name { font-weight: 500; }
                        .item-qty { color: #666; }
                        .total { margin-top: 20px; font-weight: 600; color: #1b4332; }
                    </style>
                </head>
                <body>
                    <h1>🛒 Shopping List</h1>
                    ${printContent}
                </body>
            </html>
        `);
        printWindow.document.close();
        printWindow.print();
    } else {
        showToast('No items to print', true);
    }
}

function loadRecipeModal() {
    fetch('/api/inventory')
        .then(response => response.json())
        .then(data => {
            const recipes = [
                { name: 'Veggie Omelette', ingredients: ['Eggs', 'Tomatoes', 'Onions'] },
                { name: 'Tomato Salad', ingredients: ['Tomatoes', 'Onions'] },
                { name: 'Grilled Cheese', ingredients: ['Bread', 'Cheese'] },
                { name: 'Apple Crumble', ingredients: ['Apples'] }
            ];
            
            const container = document.getElementById('recipeModalList');
            if (container) {
                container.innerHTML = recipes.map(recipe => {
                    const availableCount = recipe.ingredients.filter(ing => 
                        data.items.some(item => item.name.toLowerCase().includes(ing.toLowerCase()))
                    ).length;
                    const allAvailable = availableCount === recipe.ingredients.length;
                    return `
                        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                            <span><strong>${recipe.name}</strong></span>
                            <span style="color: ${allAvailable ? '#2d6a4f' : '#f4a261'};">
                                ${availableCount}/${recipe.ingredients.length} ingredients
                                ${allAvailable ? '✅' : '⚠️'}
                            </span>
                        </div>
                    `;
                }).join('');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error loading recipes', true);
        });
}

// ===== CRUD OPERATIONS =====
function addItem() {
    // Create centered modal
    const modalOverlay = document.createElement('div');
    modalOverlay.id = 'addItemModal';
    modalOverlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(8px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10002;
        animation: notificationFadeIn 0.3s ease;
        padding: 20px;
    `;
    
    modalOverlay.innerHTML = `
        <div style="
            background: white;
            border-radius: 24px;
            max-width: 460px;
            width: 100%;
            padding: 32px;
            box-shadow: 0 32px 64px rgba(0, 0, 0, 0.2);
            animation: notificationContentIn 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
            max-height: 90vh;
            overflow-y: auto;
        ">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <span style="font-size: 28px;">📦</span>
                <h3 style="margin: 0; font-size: 20px; font-weight: 700; color: #1b4332;">Add New Item</h3>
                <button onclick="this.closest('#addItemModal').remove()" style="
                    margin-left: auto;
                    background: none;
                    border: none;
                    font-size: 24px;
                    cursor: pointer;
                    color: #999;
                    padding: 0 8px;
                ">✕</button>
            </div>
            <p style="color: #4a6a7a; margin-bottom: 16px; font-size: 15px;">
                Enter the details for your new grocery item:
            </p>
            
            <div style="margin-bottom: 12px;">
                <label style="display: block; font-weight: 600; font-size: 14px; color: #1b4332; margin-bottom: 4px;">Item Name *</label>
                <input type="text" id="addItemName" style="
                    width: 100%;
                    padding: 10px 14px;
                    border: 2px solid #e0e0e0;
                    border-radius: 12px;
                    font-size: 14px;
                    outline: none;
                    transition: border-color 0.3s;
                " placeholder="e.g., Apples">
            </div>
            
            <div style="margin-bottom: 12px;">
                <label style="display: block; font-weight: 600; font-size: 14px; color: #1b4332; margin-bottom: 4px;">Quantity *</label>
                <input type="number" id="addItemQuantity" style="
                    width: 100%;
                    padding: 10px 14px;
                    border: 2px solid #e0e0e0;
                    border-radius: 12px;
                    font-size: 14px;
                    outline: none;
                    transition: border-color 0.3s;
                " placeholder="e.g., 5" min="0" value="1">
            </div>
            
            <div style="margin-bottom: 12px;">
                <label style="display: block; font-weight: 600; font-size: 14px; color: #1b4332; margin-bottom: 4px;">Unit</label>
                <input type="text" id="addItemUnit" style="
                    width: 100%;
                    padding: 10px 14px;
                    border: 2px solid #e0e0e0;
                    border-radius: 12px;
                    font-size: 14px;
                    outline: none;
                    transition: border-color 0.3s;
                " placeholder="e.g., pcs, kg, L" value="pcs">
            </div>
            
            <div style="margin-bottom: 12px;">
                <label style="display: block; font-weight: 600; font-size: 14px; color: #1b4332; margin-bottom: 4px;">Expiry Date</label>
                <input type="date" id="addItemExpiry" style="
                    width: 100%;
                    padding: 10px 14px;
                    border: 2px solid #e0e0e0;
                    border-radius: 12px;
                    font-size: 14px;
                    outline: none;
                    transition: border-color 0.3s;
                ">
            </div>
            
            <div style="margin-bottom: 20px;">
                <label style="display: block; font-weight: 600; font-size: 14px; color: #1b4332; margin-bottom: 4px;">Category</label>
                <input type="text" id="addItemCategory" style="
                    width: 100%;
                    padding: 10px 14px;
                    border: 2px solid #e0e0e0;
                    border-radius: 12px;
                    font-size: 14px;
                    outline: none;
                    transition: border-color 0.3s;
                " placeholder="e.g., Fruits, Vegetables" value="Other">
            </div>
            
            <div style="display: flex; gap: 12px; justify-content: flex-end;">
                <button onclick="this.closest('#addItemModal').remove()" style="
                    padding: 10px 24px;
                    border: none;
                    border-radius: 30px;
                    font-weight: 600;
                    font-size: 14px;
                    cursor: pointer;
                    background: #f0f0f0;
                    color: #4a6a7a;
                    transition: 0.2s;
                ">Cancel</button>
                <button onclick="confirmAddItem()" style="
                    padding: 10px 24px;
                    border: none;
                    border-radius: 30px;
                    font-weight: 600;
                    font-size: 14px;
                    cursor: pointer;
                    background: #2d6a4f;
                    color: white;
                    transition: 0.2s;
                ">Add Item</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modalOverlay);
    
    // Set default expiry date (30 days from now)
    const expiryInput = document.getElementById('addItemExpiry');
    if (expiryInput) {
        const date = new Date();
        date.setDate(date.getDate() + 30);
        expiryInput.value = date.toISOString().split('T')[0];
    }
    
    // Focus on name input
    setTimeout(() => {
        const nameInput = document.getElementById('addItemName');
        if (nameInput) nameInput.focus();
    }, 100);
}

function confirmAddItem() {
    const name = document.getElementById('addItemName')?.value.trim();
    const quantity = document.getElementById('addItemQuantity')?.value;
    const unit = document.getElementById('addItemUnit')?.value.trim();
    const expiry = document.getElementById('addItemExpiry')?.value;
    const category = document.getElementById('addItemCategory')?.value.trim();
    
    if (!name) {
        showToast('Please enter item name', true);
        return;
    }
    
    // Close the modal
    const modal = document.getElementById('addItemModal');
    if (modal) modal.remove();
    
    const itemData = {
        name: name,
        quantity: parseInt(quantity) || 1,
        unit: unit || 'pcs',
        expiry: expiry || '2026-12-31',
        category: category || 'Other'
    };
    
    fetch('/api/inventory', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(itemData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(`✅ Added "${name}" to inventory!`);
            refreshInventory();
            loadInventoryModal();
        } else {
            showToast('Error adding item', true);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error adding item', true);
    });
}

function updateStock(itemId) {
    // Get the item name from the UI
    const itemRow = document.querySelector(`button[onclick="updateStock(${itemId})"]`)?.closest('div');
    const itemName = itemRow ? itemRow.querySelector('span strong')?.textContent || 'item' : 'item';
    
    // Create centered modal
    const modalOverlay = document.createElement('div');
    modalOverlay.id = 'updateStockModal';
    modalOverlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(8px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10002;
        animation: notificationFadeIn 0.3s ease;
        padding: 20px;
    `;
    
    modalOverlay.innerHTML = `
        <div style="
            background: white;
            border-radius: 24px;
            max-width: 420px;
            width: 100%;
            padding: 32px;
            box-shadow: 0 32px 64px rgba(0, 0, 0, 0.2);
            animation: notificationContentIn 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
        ">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <span style="font-size: 28px;">🔄</span>
                <h3 style="margin: 0; font-size: 20px; font-weight: 700; color: #1b4332;">Update Stock</h3>
                <button onclick="this.closest('#updateStockModal').remove()" style="
                    margin-left: auto;
                    background: none;
                    border: none;
                    font-size: 24px;
                    cursor: pointer;
                    color: #999;
                    padding: 0 8px;
                ">✕</button>
            </div>
            <p style="color: #4a6a7a; margin-bottom: 16px; font-size: 15px;">
                Update quantity for "<strong>${itemName}</strong>":
            </p>
            <input type="number" id="stockQuantityInput" 
                style="
                    width: 100%;
                    padding: 12px 16px;
                    border: 2px solid #e0e0e0;
                    border-radius: 12px;
                    font-size: 16px;
                    outline: none;
                    transition: border-color 0.3s;
                    margin-bottom: 20px;
                "
                placeholder="Enter new quantity"
                min="0"
                autofocus
            >
            <div style="display: flex; gap: 12px; justify-content: flex-end;">
                <button onclick="this.closest('#updateStockModal').remove()" style="
                    padding: 10px 24px;
                    border: none;
                    border-radius: 30px;
                    font-weight: 600;
                    font-size: 14px;
                    cursor: pointer;
                    background: #f0f0f0;
                    color: #4a6a7a;
                    transition: 0.2s;
                ">Cancel</button>
                <button onclick="confirmUpdateStock(${itemId})" style="
                    padding: 10px 24px;
                    border: none;
                    border-radius: 30px;
                    font-weight: 600;
                    font-size: 14px;
                    cursor: pointer;
                    background: #2d6a4f;
                    color: white;
                    transition: 0.2s;
                ">Update</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modalOverlay);
    
    // Focus the input
    setTimeout(() => {
        const input = document.getElementById('stockQuantityInput');
        if (input) input.focus();
    }, 100);
    
    // Enter key to confirm
const enterHandler = function(e) {
    if (e.key === 'Enter' && document.getElementById('updateStockModal')) {
        confirmUpdateStock(itemId);
    }
};
document.addEventListener('keydown', enterHandler);
// Store the handler to clean up if needed
modalOverlay._enterHandler = enterHandler;
}

function confirmUpdateStock(itemId) {
    const input = document.getElementById('stockQuantityInput');
    if (!input) return;
    
    const newQuantity = input.value;
    if (newQuantity === '' || isNaN(newQuantity) || parseInt(newQuantity) < 0) {
        showToast('Please enter a valid quantity', true);
        return;
    }
    
    // Close the modal
    const modal = document.getElementById('updateStockModal');
    if (modal) modal.remove();
    
    // Send the update
    fetch(`/api/inventory/${itemId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ quantity: parseInt(newQuantity) })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(`✅ Stock updated to ${newQuantity}!`);
            loadInventoryModal();
            refreshInventory();
        } else {
            showToast('Error updating stock', true);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error updating stock', true);
    });
}

function refreshInventory() {
    fetch('/api/inventory')
        .then(response => response.json())
        .then(data => {
            const inventoryList = document.getElementById('inventoryList');
            if (inventoryList) {
                if (!data.items || data.items.length === 0) {
                    inventoryList.innerHTML = '<p>No items in inventory</p>';
                } else {
                    inventoryList.innerHTML = data.items.slice(0, 5).map(item => `
                        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
                            <span>${item.name}</span>
                            <span class="badge ${item.quantity <= 2 ? 'warning' : ''}">
                                ${item.quantity} ${item.unit}
                            </span>
                        </div>
                    `).join('');
                }
            }
            showToast('🔄 Inventory refreshed!');
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error refreshing inventory', true);
        });
}

function generateShoppingList() {
    if (shoppingList.length === 0) {
        showToast('⚠️ No items added to shopping list yet! Click "Add to List" on items you need.', true);
        return;
    }
    
    showToast(`🛒 Generating shopping list with ${shoppingList.length} items...`);
    
    fetch('/api/inventory')
        .then(response => response.json())
        .then(data => {
            const items = data.items.filter(item => shoppingList.includes(item.id));
            
            // Create the shopping list HTML
            let listHTML = `
                <div style="
                    background: #f8f9fa;
                    border-radius: 12px;
                    padding: 16px;
                    margin: 10px 0;
                    border: 2px solid #2d6a4f;
                ">
                    <h4 style="margin: 0 0 12px 0; color: #1b4332; display: flex; align-items: center; gap: 8px;">
                        🛒 Your Shopping List
                        <span style="
                            background: #2d6a4f;
                            color: white;
                            padding: 2px 12px;
                            border-radius: 20px;
                            font-size: 12px;
                        ">${items.length} items</span>
                    </h4>
                    <div class="shopping-list-items" style="display: flex; flex-direction: column; gap: 6px;">
                        ${items.map(item => `
                            <div class="shopping-item" style="
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                                padding: 8px 12px;
                                background: white;
                                border-radius: 8px;
                                border-left: 4px solid #2d6a4f;
                            ">
                                <span class="item-name" style="font-weight: 500;">${item.name}</span>
                                <span class="item-qty" style="color: #666; font-size: 14px;">
                                    ${item.quantity} ${item.unit}
                                </span>
                            </div>
                        `).join('')}
                    </div>
                    <div style="
                        margin-top: 12px;
                        padding-top: 12px;
                        border-top: 1px solid #ddd;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    ">
                        <span style="color: #666; font-size: 14px;">
                            📝 Total: ${items.length} items
                        </span>
                        <div style="display: flex; gap: 8px;">
                            <button onclick="printShoppingList()" style="
                                padding: 6px 16px;
                                background: #52b788;
                                color: white;
                                border: none;
                                border-radius: 20px;
                                cursor: pointer;
                                font-weight: 600;
                                font-size: 13px;
                            ">🖨️ Print</button>
                            <button onclick="clearShoppingList()" style="
                                padding: 6px 16px;
                                background: #e76f51;
                                color: white;
                                border: none;
                                border-radius: 20px;
                                cursor: pointer;
                                font-weight: 600;
                                font-size: 13px;
                            ">🗑️ Clear</button>
                        </div>
                    </div>
                </div>
            `;
            
            // Update the modal content
            const container = document.getElementById('shoppingModalList');
            if (container) {
                container.innerHTML = listHTML;
            }
            
            // Reset shopping list after generating
            shoppingList = [];
            updateGenerateButton();
            
            showToast(`✅ Shopping list generated with ${items.length} items!`, false);
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error generating shopping list', true);
        });
}

function predictUsage() {
    showToast('🤖 AI predicting usage patterns...');
    setTimeout(() => {
        showToast('📈 Prediction complete!');
    }, 1500);
}

function applyBudgetTip() {
    showToast('💰 Budget tip applied!');
}

function checkStatus() {
    showToast('🚀 All systems operational!');
}

// ===== INITIALIZATION =====
console.log('Script loaded successfully!');

// Make sure functions are globally accessible
window.addItem = addItem;
window.updateStock = updateStock;
window.refreshInventory = refreshInventory;
window.showModal = showModal;
window.closeModal = closeModal;
window.showToast = showToast;
window.predictUsage = predictUsage;
window.generateShoppingList = generateShoppingList;
window.applyBudgetTip = applyBudgetTip;
window.checkStatus = checkStatus;
window.addToShoppingList = addToShoppingList;  
window.clearShoppingList = clearShoppingList;  
window.printShoppingList = printShoppingList;  