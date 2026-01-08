const API_BASE_URL = 'http://127.0.0.1:8000';

// Load categories on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadCategories();
});

// Load categories from API
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/categories`);
        const data = await response.json();
        
        const categorySelect = document.getElementById('category');
        data.categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            categorySelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Handle form submission
document.getElementById('checkForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const btn = e.target.querySelector('button[type="submit"]');
    const btnText = btn.querySelector('.btn-text');
    const loader = btn.querySelector('.loader');
    
    // Show loading state
    btn.disabled = true;
    btnText.textContent = 'Checking...';
    loader.style.display = 'inline-block';
    
    // Hide previous results
    document.getElementById('results').style.display = 'none';
    
    // Get form data
    const formData = {
        product_name: document.getElementById('productName').value.trim(),
        brand: document.getElementById('brand').value.trim() || undefined,
        category: document.getElementById('category').value || undefined
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/check`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to check product');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        displayError('Unable to check product. Please make sure the API server is running on port 8000.');
    } finally {
        // Reset button state
        btn.disabled = false;
        btnText.textContent = 'Check Product';
        loader.style.display = 'none';
    }
});

// Display results
function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    const isBoycotted = data.boycott_status.is_boycotted;
    
    let html = '<div class="card">';
    
    // Boycott status
    html += `
        <div class="boycott-status ${isBoycotted ? 'boycotted' : 'safe'}">
            <div class="icon">${isBoycotted ? '⚠️' : '✅'}</div>
            <div>
                ${isBoycotted 
                    ? `<strong>${data.product_name}</strong> is on the boycott list` 
                    : `<strong>${data.product_name}</strong> is not on the boycott list`
                }
            </div>
            ${isBoycotted && data.boycott_status.reason 
                ? `<div class="reason">Reason: ${data.boycott_status.reason}</div>` 
                : ''
            }
            ${data.boycott_status.confidence 
                ? `<div class="reason">Confidence: ${(data.boycott_status.confidence * 100).toFixed(0)}%</div>` 
                : ''
            }
        </div>
    `;
    
    // Alternatives section
    if (data.alternatives && data.alternatives.length > 0) {
        html += `
            <div class="alternatives-section">
                <h3>🇹🇳 Tunisian Alternatives</h3>
                <div class="product-grid">
        `;
        
        data.alternatives.forEach(product => {
            html += `
                <div class="product-card">
                    <h4>${product.name}</h4>
                    <div class="brand">${product.brand}</div>
                    <span class="category">${product.category}</span>
                    ${product.rating ? `<div class="rating">⭐ ${product.rating}/5</div>` : ''}
                    ${product.description ? `<p class="description">${product.description}</p>` : ''}
                    <div style="margin-top: 0.5rem; font-size: 0.85rem; color: var(--success-color); font-weight: 600;">
                        🇹🇳 Made in Tunisia
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    }
    
    html += '</div>';
    
    resultsDiv.innerHTML = html;
    resultsDiv.style.display = 'block';
    
    // Smooth scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Display error message
function displayError(message) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <div class="card">
            <div class="error-message">
                <strong>Error:</strong> ${message}
            </div>
        </div>
    `;
    resultsDiv.style.display = 'block';
}
