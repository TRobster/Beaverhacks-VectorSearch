// Global variable to store card data
let cardData = [];
let filteredCardData = [];

// Load card data when the page loads
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const response = await fetch('cards.json');
    cardData = await response.json();
    filteredCardData = [...cardData]; // Initialize filtered data with all cards
    console.log('Card data loaded:', cardData);
    
    // Set up search input event listener
    const searchInput = document.getElementById('filter-text');
    if (searchInput) {
      searchInput.addEventListener('input', handleSearch);
    }
    
    // Initial display of cards
    displayCards();
  } catch (error) {
    console.error('Error loading card data:', error);
  }
});

// Handle search input
function handleSearch(event) {
  const searchTerm = event.target.value.toLowerCase();
  
  // Filter cards based on search term
  filteredCardData = cardData.filter(card => 
    card.title.toLowerCase().includes(searchTerm)
  );
  
  console.log('Filtered cards:', filteredCardData);
  
  // Update the display immediately when searching
  displayCards();
}

// Add event listener to the update button
const updateButton = document.getElementById("filter-update-button");
if (updateButton) {
  updateButton.addEventListener("click", () => {
    const searchInput = document.getElementById('filter-text');
    if (searchInput) {
      const searchTerm = searchInput.value.toLowerCase();
      filteredCardData = cardData.filter(card => 
        card.title.toLowerCase().includes(searchTerm)
      );
      displayCards();
    }
  });
}

// Function to display cards
function displayCards() {
  console.log("Displaying cards:", filteredCardData);
  
  // Get the posts section
  const postsSection = document.getElementById('posts');
  
  // Clear existing posts
  postsSection.innerHTML = '';
  
  // If no cards match the search, show a message
  if (filteredCardData.length === 0) {
    const noResultsMessage = document.createElement('div');
    noResultsMessage.className = 'post';
    noResultsMessage.innerHTML = `
      <div class="post-contents">
        <div class="post-info-container">
          <h3>No cards found matching your search.</h3>
        </div>
      </div>
    `;
    postsSection.appendChild(noResultsMessage);
    return;
  }
  
  // Create a post for each card
  filteredCardData.forEach(card => {
    const postElement = document.createElement('div');
    postElement.className = 'post';
    postElement.innerHTML = `
      <div class="post-contents">
        <div class="post-image-container">
          <img src="${card.imageUrl}" alt="${card.title}" class="card-image">
        </div>
        <div class="post-info-container">
          <a href="#" class="post-title">${card.title}</a>
        </div>
      </div>
    `;
    postsSection.appendChild(postElement);
  });
}
