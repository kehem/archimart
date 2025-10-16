let yourProductsData = [];
let alternateProductsData = [];
let selectedYourProducts = [];
let selectedAlternateProducts = [];
let yourChoiceConfirmed = false;
let archimartChoiceConfirmed = false;

// Initialize cartItems from localStorage (same as cart.html)
let cartItems = [];
function loadInitialCart() {
  try {
    const savedCart = localStorage.getItem('cartState');
    console.log('Loaded cartState from localStorage:', savedCart);
    if (savedCart) {
      cartItems = JSON.parse(savedCart);
      cartItems.forEach((item, index) => {
        if (!item.price || typeof item.price !== 'number' || item.price <= 0) {
          console.error(`Invalid price for item ${item.name} at index ${index}: ${item.price}`);
          item.price = 0;
        }
      });
    } else {
      cartItems = [];
    }
  } catch (e) {
    console.error("Error loading cart state:", e);
    cartItems = [];
  }
  console.log('cartItems for compare:', cartItems);
}

// ✅ DYNAMIC ID EXTRACTION + API FETCH
async function loadProductsFromAPI() {
  if (cartItems.length === 0) {
    console.error('No cart items found');
    showNotification('Cart is empty! Add items first.');
    return;
  }

  // 🔑 EXTRACT ALL PRODUCT IDs DYNAMICALLY (no hardcoding!)
  const productIds = cartItems
    .map(item => item.id || item.product_id)  // Try both id & product_id
    .filter(id => id !== undefined && id !== null && id !== '')  // Valid IDs only
    .slice(0, 4);  // Max 4 products for comparison
  
  if (productIds.length === 0) {
    console.error('No valid product IDs found');
    showNotification('No product IDs found in cart!');
    return;
  }

  const productList = productIds.join(',');  // e.g., "23,45,67,89"
  console.log('🔑 DYNAMIC Product IDs:', productIds);
  console.log('📡 Fetching API:', `alternate_product?product_list=${productList}`);

  // Show loading
  const header = document.querySelector('.header');
  header.textContent = 'Loading alternate products...';

  try {
    const params = new URLSearchParams(window.location.search);
    const option = params.get('option') || 'default'; // 'high' or 'low'

    // Build the URL dynamically
    const response = await fetch(
      `https://archimartbd.com/api/alternative?product_list=${encodeURIComponent(productList)}&option=${encodeURIComponent(option)}`
    );
    
    if (!response.ok) {
      throw new Error(`API failed: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('📦 API Response:', data);

    // 📋 Process API response with original and alternative products
    if (Array.isArray(data) && data.length > 0) {
      // YOUR PRODUCTS = From API response "original" field
      yourProductsData = data.slice(0, 4).map((apiItem, index) => {
        const original = apiItem.original || {};
        return {
          id: original.id || `item-${index}`,
          name: original.name || `Item ${index + 1}`,
          brand: original.brand || "Archimart",
          price: original.price || 0,
          quantity: 1,
          images: original.images || []
        };
      });

      // ALTERNATE PRODUCTS = From API response "alternative" field
      alternateProductsData = data.slice(0, 4).map((apiItem, index) => {
        const alternative = apiItem.alternative;
        
        // Check if alternative is a string (message) or object (product)
        if (typeof alternative === 'string') {
          // No alternative available - return message object
          return {
            id: null,
            name: alternative, // Display the message
            brand: '-',
            price: 0,
            quantity: 0,
            images: [],
            isMessage: true, // Flag to identify message rows
            isAvailable: false
          };
        } else if (alternative && typeof alternative === 'object') {
          // Alternative product exists
          return {
            id: alternative.id || `alt-${index}`,
            name: alternative.name || `Premium Item ${index + 1}`,
            brand: alternative.brand || "Archimart",
            price: alternative.price || 0,
            quantity: 1,
            images: alternative.images || [],
            isMessage: false,
            isAvailable: true
          };
        } else {
          // Fallback if alternative is undefined/null
          return {
            id: null,
            name: 'No alternative available',
            brand: '-',
            price: 0,
            quantity: 0,
            images: [],
            isMessage: true,
            isAvailable: false
          };
        }
      });
    } else {
      // Fallback: Use cart items if API fails
      yourProductsData = cartItems.slice(0, 4).map((item, index) => ({
        id: item.id || item.product_id || `item-${index}`,
        name: item.name || `Item ${index + 1}`,
        brand: item.brand || "Archimart",
        price: item.price || 0,
        quantity: item.quantity || 1
      }));

      // Fallback: 36% higher price versions
      alternateProductsData = yourProductsData.map(item => ({
        id: `alt-${item.id}`,
        name: `Premium ${item.name}`,
        brand: item.brand,
        price: Math.round(item.price * 1.36),
        quantity: 1
      }));
    }

    console.log('✅ Your Products:', yourProductsData);
    console.log('✅ Alternate Products:', alternateProductsData);

  } catch (error) {
    console.error('❌ API Error:', error);
    
    // 🛡️ SMART FALLBACK
    yourProductsData = cartItems.slice(0, 4).map((item, index) => ({
      id: item.id || item.product_id || `item-${index}`,
      name: item.name || `Item ${index + 1}`,
      brand: item.brand || "Archimart",
      price: item.price || 550,
      quantity: item.quantity || 1
    }));

    alternateProductsData = yourProductsData.map(item => ({
      id: `alt-${item.id}`,
      name: `Premium ${item.name}`,
      brand: item.brand,
      price: Math.round(item.price * 1.36),
      quantity: 1
    }));

    showNotification('⚠️ Using premium fallback (API unavailable)');
  }

  // Update header back to normal
  document.querySelector('.header').textContent = 'Alternate option with higher price';
  updateAllTables();
  showNotification(`Loaded ${yourProductsData.length} products for comparison!`);
}

function initializeQuantityControls() {
  document.querySelectorAll('.qty-btn-your').forEach(btn => {
    btn.addEventListener('click', function() {
      const index = parseInt(this.dataset.index);
      const change = parseInt(this.dataset.change);
      changeProductQuantity('your', index, change);
    });
  });

  document.querySelectorAll('.qty-btn-alt').forEach(btn => {
    btn.addEventListener('click', function() {
      const index = parseInt(this.dataset.index);
      const change = parseInt(this.dataset.change);
      changeProductQuantity('alternate', index, change);
    });
  });
}

function changeProductQuantity(type, index, change) {
  if (type === 'your' && index >= 0 && index < yourProductsData.length) {
    yourProductsData[index].quantity = Math.max(1, yourProductsData[index].quantity + change);
  } else if (type === 'alternate' && index >= 0 && index < alternateProductsData.length) {
    alternateProductsData[index].quantity = Math.max(1, alternateProductsData[index].quantity + change);
  }
  
  updateAllTables();
  updateSelection('your-products');
  updateSelection('alternate-products');
}

function updateAllTables() {
  const yourTable = document.getElementById('your-products-table');
  yourTable.innerHTML = '';
  yourProductsData.forEach((item, index) => {
    const totalPrice = item.price * item.quantity;
    yourTable.innerHTML += `
      <tr class="product-row" data-price="${totalPrice}">
        <td>${index + 1}. ${item.name}</td>
        <td>${item.brand}</td>
        <td>${item.price}/- × ${item.quantity} = ${totalPrice}/-</td>
        <td>
          <div style="display: flex; align-items: center; gap: 5px; justify-content: center;">
            <button class="qty-btn qty-btn-your" data-index="${index}" data-change="-1">−</button>
            <span style="min-width: 25px; text-align: center;">${item.quantity}</span>
            <button class="qty-btn qty-btn-your" data-index="${index}" data-change="1">+</button>
          </div>
        </td>
        <td><input type="checkbox" class="select-checkbox your-products" data-index="${index}" data-price="${totalPrice}"></td>
      </tr>
    `;
  });

  const altTable = document.getElementById('alternate-products-table');
  altTable.innerHTML = '';
  alternateProductsData.forEach((item, index) => {
    // Check if this is a message row (no alternative available)
    if (item.isMessage) {
      altTable.innerHTML += `
        <tr class="product-row message-row" style="background: #fff3e3; opacity: 0.7;">
          <td colspan="3" style="text-align: center; font-style: italic; color: #8B4513;">
            ${item.name}
          </td>
          <td>-</td>
          <td>
            <input type="checkbox" class="select-checkbox alternate-products" 
                   data-index="${index}" disabled style="cursor: not-allowed;">
          </td>
        </tr>
      `;
    } else {
      // Normal product row
      const totalPrice = item.price * item.quantity;
      altTable.innerHTML += `
        <tr class="product-row" data-price="${totalPrice}">
          <td>${index + 1}. ${item.name}</td>
          <td>${item.brand}</td>
          <td>${item.price}/- × ${item.quantity} = ${totalPrice}/-</td>
          <td>
            <div style="display: flex; align-items: center; gap: 5px; justify-content: center;">
              <button class="qty-btn qty-btn-alt" data-index="${index}" data-change="-1">−</button>
              <span style="min-width: 25px; text-align: center;">${item.quantity}</span>
              <button class="qty-btn qty-btn-alt" data-index="${index}" data-change="1">+</button>
            </div>
          </td>
          <td><input type="checkbox" class="select-checkbox alternate-products" data-index="${index}" data-price="${totalPrice}"></td>
        </tr>
      `;
    }
  });

  initializeQuantityControls();
}

function initializeCheckboxListeners() {
  document.addEventListener('change', function(e) {
    if (e.target.classList.contains('your-products')) {
      updateSelection('your-products');
      updateRowHighlight(e.target);
    } else if (e.target.classList.contains('alternate-products')) {
      updateSelection('alternate-products');
      updateRowHighlight(e.target);
    }
  });
}

function initializeButtonListeners() {
  document.getElementById('select-your-choice').addEventListener('click', confirmYourChoice);
  document.getElementById('archimart-choice').addEventListener('click', confirmArchimartChoice);
  document.getElementById('combined-selection').addEventListener('click', createCombinedSelection);
}

function updateRowHighlight(checkbox) {
  const row = checkbox.closest('.product-row');
  if (checkbox.checked) {
    row.classList.add('selected');
  } else {
    row.classList.remove('selected');
  }
}

function updateSelection(type) {
  const checkboxes = document.querySelectorAll(`.${type}`);
  let total = 0;
  let selectedItems = [];

  checkboxes.forEach(checkbox => {
    if (checkbox.checked && !checkbox.disabled) {
      const price = parseInt(checkbox.dataset.price);
      const index = parseInt(checkbox.dataset.index);
      total += price;
      
      if (type === 'your-products') {
        const item = yourProductsData[index];
        selectedItems.push({
          id: item.id,
          name: item.name,
          price: item.price,
          quantity: item.quantity,
          totalPrice: item.price * item.quantity,
          type: 'your'
        });
      } else {
        const item = alternateProductsData[index];
        // Skip if it's a message row
        if (!item.isMessage && item.isAvailable) {
          selectedItems.push({
            id: item.id,
            name: item.name,
            price: item.price,
            quantity: item.quantity,
            totalPrice: item.price * item.quantity,
            type: 'alternate'
          });
        }
      }
    }
  });

  if (type === 'your-products') {
    selectedYourProducts = selectedItems;
    document.getElementById('your-total').textContent = `${total}/-`;
    document.getElementById('select-your-choice').disabled = selectedItems.length === 0;
  } else {
    selectedAlternateProducts = selectedItems;
    document.getElementById('alternate-total').textContent = `${total}/-`;
    document.getElementById('archimart-choice').disabled = selectedItems.length === 0;
  }

  updateCombinedSection();
}

function confirmYourChoice() {
  if (selectedYourProducts.length === 0) return;
  
  yourChoiceConfirmed = true;
  const button = document.getElementById('select-your-choice');
  const totalItems = selectedYourProducts.reduce((sum, item) => sum + item.quantity, 0);
  button.textContent = `✓ Your Choice Confirmed (${totalItems} items)`;
  button.style.background = '#28a745';
  
  document.querySelectorAll('.your-products').forEach(checkbox => {
    if (!checkbox.checked) {
      checkbox.disabled = true;
      checkbox.closest('.product-row').style.opacity = '0.5';
    }
  });

  document.querySelectorAll('.qty-btn-your').forEach(btn => {
    const index = parseInt(btn.dataset.index);
    const isSelected = selectedYourProducts.some(item => yourProductsData[index]?.id === item.id);
    if (!isSelected) {
      btn.disabled = true;
      btn.style.opacity = '0.5';
    }
  });

  updateCombinedSection();
  showNotification('Your choice has been confirmed!');
}

function confirmArchimartChoice() {
  if (selectedAlternateProducts.length === 0) return;
  
  archimartChoiceConfirmed = true;
  const button = document.getElementById('archimart-choice');
  const totalItems = selectedAlternateProducts.reduce((sum, item) => sum + item.quantity, 0);
  button.textContent = `✓ Archimart Choice Confirmed (${totalItems} items)`;
  button.style.background = '#28a745';
  
  document.querySelectorAll('.alternate-products').forEach(checkbox => {
    if (!checkbox.checked) {
      checkbox.disabled = true;
      checkbox.closest('.product-row').style.opacity = '0.5';
    }
  });

  document.querySelectorAll('.qty-btn-alt').forEach(btn => {
    const index = parseInt(btn.dataset.index);
    const isSelected = selectedAlternateProducts.some(item => alternateProductsData[index]?.id === item.id);
    if (!isSelected) {
      btn.disabled = true;
      btn.style.opacity = '0.5';
    }
  });

  updateCombinedSection();
  showNotification('Archimart choice has been confirmed!');
}

function updateCombinedSection() {
  const yourTotal = selectedYourProducts.reduce((sum, item) => sum + item.totalPrice, 0);
  const alternateTotal = selectedAlternateProducts.reduce((sum, item) => sum + item.totalPrice, 0);
  const combinedTotal = yourTotal + alternateTotal;

  document.getElementById('combined-total').textContent = `${combinedTotal}/-`;
  
  const combinedButton = document.getElementById('combined-selection');
  const canCreateCombined = selectedYourProducts.length > 0 || selectedAlternateProducts.length > 0;
  
  combinedButton.disabled = !canCreateCombined;
  
  if (canCreateCombined) {
    const totalItems = selectedYourProducts.reduce((sum, item) => sum + item.quantity, 0) + 
                      selectedAlternateProducts.reduce((sum, item) => sum + item.quantity, 0);
    combinedButton.textContent = `Create Combined Selection (${totalItems} items)`;
    combinedButton.style.background = '#8B4513';
  } else {
    combinedButton.textContent = 'Create Combined Selection';
    combinedButton.style.background = '#ccc';
  }
}

function createCombinedSelection() {
  if (selectedYourProducts.length === 0 && selectedAlternateProducts.length === 0) {
    showNotification('Please select at least one item from either section!');
    return;
  }

  const combinedItems = [...selectedYourProducts, ...selectedAlternateProducts];
  const totalAmount = combinedItems.reduce((sum, item) => sum + item.totalPrice, 0);
  
  const combinedSelection = {
    items: combinedItems,
    totalAmount: totalAmount,
    yourProducts: selectedYourProducts,
    alternateProducts: selectedAlternateProducts,
    timestamp: new Date().toISOString()
  };

  try {
    localStorage.setItem('combinedSelection', JSON.stringify(combinedSelection));
  } catch (e) {
    console.error('Failed to save to localStorage:', e);
    showNotification('Error saving selection. Proceeding to cart...');
  }

  const combinedButton = document.getElementById('combined-selection');
  combinedButton.textContent = '✓ Combined Selection Created!';
  combinedButton.style.background = '#28a745';
  combinedButton.disabled = true;
  
  const totalItems = combinedItems.reduce((sum, item) => sum + item.quantity, 0);
  showNotification(`Combined selection created! Total: ${totalAmount}/- (${totalItems} items)`);
  
  setTimeout(() => {
    window.location.href = 'https://archimartbd.com/cart?combined=true';
  }, 1500);
}

function showNotification(message) {
  const notification = document.createElement('div');
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #28a745;
    color: white;
    padding: 15px 20px;
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    z-index: 1000;
    font-size: 14px;
    font-weight: 500;
    max-width: 300px;
    animation: slideIn 0.3s ease;
  `;
  
  notification.textContent = message;
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => {
      if (document.body.contains(notification)) {
        document.body.removeChild(notification);
      }
    }, 300);
  }, 3000);
}

// 🚀 INITIALIZE
document.addEventListener('DOMContentLoaded', async function() {
  loadInitialCart();
  await loadProductsFromAPI();
  initializeCheckboxListeners();
  initializeButtonListeners();
  
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
    @keyframes slideOut { from { transform: translateX(0); opacity: 1; } to { transform: translateX(100%); opacity: 0; } }
    .qty-btn { width: 22px; height: 22px; border: 1px solid #d4a574; background: #f9f9f9; cursor: pointer; font-size: 14px; font-weight: bold; color: #8B4513; display: flex; align-items: center; justify-content: center; border-radius: 3px; }
    .qty-btn:hover:not(:disabled) { background: #e6d7c3; }
    .qty-btn:disabled { cursor: not-allowed; opacity: 0.5; }
    .product-row.selected { background: #fff3e3; border-left: 4px solid #d4a574; }
  `;
  document.head.appendChild(style);
});