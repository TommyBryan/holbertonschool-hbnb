/* 
  HBNB Application JavaScript
  Handles login functionality, main page place listings with filtering, and place details
*/

document.addEventListener('DOMContentLoaded', () => {
    // Check if we're on the login page
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        // Login page functionality
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Get form values
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Validate inputs
            if (!email || !password) {
                alert('Please enter both email and password');
                return;
            }
            
            // Call login function
            await loginUser(email, password);
        });
        
        // Check if user is already logged in
        checkAuthStatus();
    }
    
    // Check if we're on the main page (index.html)
    const placesList = document.getElementById('places-list');
    if (placesList) {
        // Main page functionality
        initializeMainPage();
    }
    
    // Check if we're on the place details page (place.html)
    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
        // Place details page functionality
        initializePlaceDetailsPage();
    }
    
    // Check if we're on the add review page (add_review.html)
    const addReviewForm = document.getElementById('review-form');
    const placeSummary = document.getElementById('place-summary');
    if (addReviewForm && placeSummary) {
        // Add review page functionality
        initializeAddReviewPage();
    }
});

// ========== LOGIN FUNCTIONALITY ==========

async function loginUser(email, password) {
    try {
        // Make API request to login endpoint
        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        // Handle the response
        if (response.ok) {
            const data = await response.json();
            
            // Store JWT token in cookie
            document.cookie = `token=${data.access_token}; path=/; max-age=86400`; // 24 hours
            
            // Redirect to main page
            window.location.href = 'index.html';
        } else {
            // Handle login failure
            const errorData = await response.json();
            const errorMessage = errorData.error || 'Login failed';
            alert('Login failed: ' + errorMessage);
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('An error occurred while logging in. Please try again.');
    }
}

// ========== MAIN PAGE FUNCTIONALITY ==========

// Store places data globally for filtering
let allPlaces = [];

function initializeMainPage() {
    // Check authentication and setup page
    checkAuthentication();
    
    // Initialize price filter dropdown
    initializePriceFilter();
    
    // Add event listener for price filtering
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            filterPlacesByPrice(event.target.value);
        });
    }
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');

    if (!token) {
        // User not authenticated - show login link, hide logout link
        if (loginLink) loginLink.style.display = 'block';
        if (logoutLink) logoutLink.style.display = 'none';
        
        // Still fetch places even if not authenticated (assuming public access)
        fetchPlaces();
    } else {
        // User authenticated - hide login link, show logout link
        if (loginLink) loginLink.style.display = 'none';
        if (logoutLink) logoutLink.style.display = 'block';
        
        // Fetch places data with token
        fetchPlaces(token);
    }
}

async function fetchPlaces(token = null) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Include token in Authorization header if available
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch('/api/v1/places/', {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            allPlaces = places; // Store globally for filtering
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
            // Show error message to user
            const placesList = document.getElementById('places-list');
            if (placesList) {
                placesList.innerHTML = '<p>Failed to load places. Please try again later.</p>';
            }
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        const placesList = document.getElementById('places-list');
        if (placesList) {
            placesList.innerHTML = '<p>An error occurred while loading places. Please try again later.</p>';
        }
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    // Clear the current content
    placesList.innerHTML = '';
    
    if (places.length === 0) {
        placesList.innerHTML = '<p>No places available at the moment.</p>';
        return;
    }
    
    // Iterate over the places data and create elements
    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.setAttribute('data-price', place.price);
        
        placeCard.innerHTML = `
            <h3>${escapeHtml(place.title)}</h3>
            <p class="description">${escapeHtml(place.description || 'No description available')}</p>
            <p class="price">$${place.price}/night</p>
            <div class="place-actions">
                <button class="details-button" onclick="viewPlaceDetails('${place.id}')">View Details</button>
                <button class="review-button" onclick="addReviewForPlace('${place.id}')">Add Review</button>
            </div>
        `;
        
        placesList.appendChild(placeCard);
    });
}

function initializePriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;
    
    // Clear existing options
    priceFilter.innerHTML = '';
    
    // Add price filter options
    const options = [
        { value: 'all', text: 'All' },
        { value: '10', text: '$10' },
        { value: '50', text: '$50' },
        { value: '100', text: '$100' }
    ];
    
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option.value;
        optionElement.textContent = option.text;
        priceFilter.appendChild(optionElement);
    });
}

function filterPlacesByPrice(maxPrice) {
    const placeCards = document.querySelectorAll('.place-card');
    
    placeCards.forEach(card => {
        const placePrice = parseFloat(card.getAttribute('data-price'));
        
        if (maxPrice === 'all') {
            // Show all places
            card.style.display = 'block';
        } else {
            const maxPriceValue = parseFloat(maxPrice);
            if (placePrice <= maxPriceValue) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        }
    });
}

// ========== UTILITY FUNCTIONS ==========

// Utility function to get cookie value
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Check if user is already authenticated (for login page)
function checkAuthStatus() {
    const token = getCookie('token');
    if (token && window.location.pathname.includes('login.html')) {
        // User is already logged in, redirect to home page
        window.location.href = 'index.html';
    }
}

// Logout function
function logout() {
    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    window.location.href = 'login.html';
}

// Escape HTML to prevent XSS attacks
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

// Function to view place details (placeholder)
function viewPlaceDetails(placeId) {
    // Navigate to place details page with place ID as query parameter
    window.location.href = `place.html?id=${placeId}`;
}

// Function to add review for a place
function addReviewForPlace(placeId) {
    // Check if user is authenticated
    const token = getCookie('token');
    if (!token) {
        alert('You must be logged in to add a review. Please log in first.');
        window.location.href = 'login.html';
        return;
    }
    
    // Navigate to add review page with place ID as query parameter
    window.location.href = `add_review.html?id=${placeId}`;
}

// ========== PLACE DETAILS PAGE FUNCTIONALITY ==========

function initializePlaceDetailsPage() {
    // Get place ID from URL
    const placeId = getPlaceIdFromURL();
    
    if (!placeId) {
        alert('Invalid place ID');
        window.location.href = 'index.html';
        return;
    }
    
    // Check authentication and setup page
    checkAuthenticationForPlace(placeId);
    
    // Setup review form submission if it exists
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            await submitReview(placeId);
        });
    }
}

function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

function checkAuthenticationForPlace(placeId) {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        // User not authenticated - show login link, hide logout link and review form
        if (loginLink) loginLink.style.display = 'block';
        if (logoutLink) logoutLink.style.display = 'none';
        if (addReviewSection) addReviewSection.style.display = 'none';
        
        // Fetch place details without token
        fetchPlaceDetails(null, placeId);
    } else {
        // User authenticated - hide login link, show logout link and review form
        if (loginLink) loginLink.style.display = 'none';
        if (logoutLink) logoutLink.style.display = 'block';
        if (addReviewSection) addReviewSection.style.display = 'block';
        
        // Fetch place details with token
        fetchPlaceDetails(token, placeId);
    }
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Include token in Authorization header if available
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            await displayPlaceDetails(place);
            
            // Fetch reviews for this place
            await fetchPlaceReviews(placeId);
        } else if (response.status === 404) {
            alert('Place not found');
            window.location.href = 'index.html';
        } else {
            console.error('Failed to fetch place details:', response.statusText);
            alert('Failed to load place details. Please try again later.');
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        alert('An error occurred while loading place details. Please try again later.');
    }
}

async function displayPlaceDetails(place) {
    const placeDetailsSection = document.querySelector('#place-details .place-info');
    if (!placeDetailsSection) return;
    
    // Clear existing content
    placeDetailsSection.innerHTML = '';
    
    // Get owner information
    let ownerName = 'Unknown Host';
    try {
        const ownerResponse = await fetch(`/api/v1/users/${place.owner_id}`);
        if (ownerResponse.ok) {
            const owner = await ownerResponse.json();
            ownerName = `${owner.first_name} ${owner.last_name}`;
        }
    } catch (error) {
        console.error('Error fetching owner details:', error);
    }
    
    // Create place details HTML
    const placeHTML = `
        <h1>${escapeHtml(place.title)}</h1>
        <p>Hosted by <span class="host-name">${escapeHtml(ownerName)}</span></p>
        <p class="price">$${place.price}/night</p>
        <p class="description">${escapeHtml(place.description || 'No description available')}</p>
        <div class="location">
            <p><strong>Location:</strong> Latitude: ${place.latitude}, Longitude: ${place.longitude}</p>
        </div>
        <div class="amenities-section">
            <h3>Amenities</h3>
            <ul class="amenities" id="amenities-list">
                <li>Loading amenities...</li>
            </ul>
        </div>
    `;
    
    placeDetailsSection.innerHTML = placeHTML;
    
    // Fetch and display amenities
    await fetchPlaceAmenities(place.id);
}

async function fetchPlaceAmenities(placeId) {
    try {
        const response = await fetch(`/api/v1/places/${placeId}`);
        if (response.ok) {
            const place = await response.json();
            const amenitiesList = document.getElementById('amenities-list');
            
            if (amenitiesList) {
                if (place.amenities && place.amenities.length > 0) {
                    amenitiesList.innerHTML = place.amenities.map(amenity => 
                        `<li>${escapeHtml(amenity.name)}</li>`
                    ).join('');
                } else {
                    amenitiesList.innerHTML = '<li>No amenities listed</li>';
                }
            }
        }
    } catch (error) {
        console.error('Error fetching amenities:', error);
        const amenitiesList = document.getElementById('amenities-list');
        if (amenitiesList) {
            amenitiesList.innerHTML = '<li>Failed to load amenities</li>';
        }
    }
}

async function fetchPlaceReviews(placeId) {
    try {
        const response = await fetch(`/api/v1/reviews/places/${placeId}/reviews`);
        
        if (response.ok) {
            const reviews = await response.json();
            displayReviews(reviews);
        } else {
            console.error('Failed to fetch reviews:', response.statusText);
            displayReviews([]);
        }
    } catch (error) {
        console.error('Error fetching reviews:', error);
        displayReviews([]);
    }
}

function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');
    if (!reviewsList) return;
    
    // Clear existing content
    reviewsList.innerHTML = '';
    
    if (reviews.length === 0) {
        reviewsList.innerHTML = '<p>No reviews yet. Be the first to review this place!</p>';
        return;
    }
    
    // Create review cards
    reviews.forEach(async (review) => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        
        // Get reviewer information
        let reviewerName = 'Anonymous User';
        try {
            const userResponse = await fetch(`/api/v1/users/${review.user_id}`);
            if (userResponse.ok) {
                const user = await userResponse.json();
                reviewerName = `${user.first_name} ${user.last_name}`;
            }
        } catch (error) {
            console.error('Error fetching reviewer details:', error);
        }
        
        reviewCard.innerHTML = `
            <p class="review-comment">${escapeHtml(review.text)}</p>
            <p class="review-user">By ${escapeHtml(reviewerName)}</p>
            <p class="review-rating">Rating: ${review.rating}/5</p>
            <p class="review-date">Posted on: ${new Date(review.created_at).toLocaleDateString()}</p>
        `;
        
        reviewsList.appendChild(reviewCard);
    });
}

async function submitReview(placeId) {
    const token = getCookie('token');
    if (!token) {
        alert('You must be logged in to submit a review');
        return;
    }
    
    const reviewText = document.getElementById('review-text').value.trim();
    const reviewRating = document.getElementById('review-rating').value;
    
    if (!reviewText) {
        alert('Please enter a review text');
        return;
    }
    
    if (!reviewRating) {
        alert('Please select a rating');
        return;
    }
    
    try {
        const response = await fetch('/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(reviewRating),
                place_id: placeId
            })
        });
        
        if (response.ok) {
            alert('Review submitted successfully!');
            document.getElementById('review-text').value = ''; // Clear the form
            document.getElementById('review-rating').value = ''; // Clear the rating
            
            // Refresh the reviews list
            await fetchPlaceReviews(placeId);
        } else {
            const errorData = await response.json();
            const errorMessage = errorData.error || 'Failed to submit review';
            alert('Failed to submit review: ' + errorMessage);
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('An error occurred while submitting your review. Please try again.');
    }
}

// ========== ADD REVIEW PAGE FUNCTIONALITY ==========

function initializeAddReviewPage() {
    // Check authentication - redirect if not authenticated
    const token = checkAuthenticationForReview();
    if (!token) return;
    
    // Get place ID from URL
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        alert('Invalid place ID');
        window.location.href = 'index.html';
        return;
    }
    
    // Setup authentication UI
    setupAuthenticationUI(token);
    
    // Fetch and display place summary
    fetchPlaceSummary(placeId);
    
    // Setup review form submission
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            await submitReviewFromForm(token, placeId);
        });
    }
}

function checkAuthenticationForReview() {
    const token = getCookie('token');
    if (!token) {
        // Redirect unauthenticated users to index page
        window.location.href = 'index.html';
        return null;
    }
    return token;
}

function setupAuthenticationUI(token) {
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    
    if (token) {
        // User authenticated - hide login link, show logout link
        if (loginLink) loginLink.style.display = 'none';
        if (logoutLink) logoutLink.style.display = 'block';
    } else {
        // User not authenticated - show login link, hide logout link
        if (loginLink) loginLink.style.display = 'block';
        if (logoutLink) logoutLink.style.display = 'none';
    }
}

async function fetchPlaceSummary(placeId) {
    try {
        const response = await fetch(`/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceSummary(place);
        } else if (response.status === 404) {
            alert('Place not found');
            window.location.href = 'index.html';
        } else {
            console.error('Failed to fetch place details:', response.statusText);
            alert('Failed to load place information. Please try again later.');
        }
    } catch (error) {
        console.error('Error fetching place summary:', error);
        alert('An error occurred while loading place information. Please try again later.');
    }
}

function displayPlaceSummary(place) {
    const placeSummary = document.getElementById('place-summary');
    if (!placeSummary) return;
    
    placeSummary.innerHTML = `
        <div class="place-summary-content">
            <h3>You are reviewing:</h3>
            <h2>${escapeHtml(place.title)}</h2>
            <p class="price">$${place.price}/night</p>
            <p class="description">${escapeHtml(place.description || 'No description available')}</p>
        </div>
    `;
}

async function submitReviewFromForm(token, placeId) {
    const reviewText = document.getElementById('review').value.trim();
    const reviewRating = document.getElementById('rating').value;
    
    if (!reviewText) {
        alert('Please enter a review text');
        return;
    }
    
    if (!reviewRating) {
        alert('Please select a rating');
        return;
    }
    
    try {
        const response = await fetch('/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(reviewRating),
                place_id: placeId
            })
        });
        
        if (response.ok) {
            alert('Review submitted successfully!');
            
            // Clear the form
            document.getElementById('review').value = '';
            document.getElementById('rating').value = '';
            
            // Optionally redirect back to place details page
            const redirectToPlace = confirm('Review submitted! Would you like to view the place details?');
            if (redirectToPlace) {
                window.location.href = `place.html?id=${placeId}`;
            }
        } else {
            const errorData = await response.json();
            const errorMessage = errorData.error || 'Failed to submit review';
            alert('Failed to submit review: ' + errorMessage);
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('An error occurred while submitting your review. Please try again.');
    }
}
