// Global variable to store card data
let cardData = [];

// Load card data when the page loads
document.addEventListener('DOMContentLoaded', async () => {
  try {
    // Fetch all cards from the JSON file
    const response = await fetch('cards.json');
    cardData = await response.json();
    console.log('Card data loaded:', cardData);
    
    // Set up search input event listener with debounce
    const searchInput = document.getElementById('filter-text');
    if (searchInput) {
      searchInput.addEventListener('input', debounce(handleSearch, 300));
    }
    
    // Initial display of cards
    updateImages(cardData);
  } catch (error) {
    console.error('Error loading card data:', error);
  }
});

// Debounce function to limit how often the search function is called
function debounce(func, delay) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), delay);
  };
}

// Handle search input
function handleSearch(event) {
  const searchTerm = event.target.value.toLowerCase();
  
  // Filter cards based on search term
  const filteredCards = cardData.filter(card => 
    card.title.toLowerCase().includes(searchTerm)
  );
  
  console.log('Filtered cards:', filteredCards);
  
  // Update the display with filtered cards
  updateImages(filteredCards);
}

const button = document.getElementById("filter-update-button");
button.addEventListener("click", () => {
  // When button is clicked, show all cards again
  updateImages(cardData);
});

function updateImages(cards) {
  console.log("Updating images with card data");
  
  // Get all post elements
  const posts = document.querySelectorAll('.post');
  
  // Update each post with data from the cards array
  posts.forEach((post, index) => {
    if (index < cards.length) {
      // Get the image and title elements
      const imgElement = post.querySelector('img');
      const titleElement = post.querySelector('.post-title');
      
      // Update the image source and title
      if (imgElement) {
        imgElement.src = cards[index].imageUrl;
        imgElement.alt = cards[index].title;
      }
      
      if (titleElement) {
        titleElement.textContent = cards[index].title;
      }
      
      // Show the post
      post.style.display = 'block';
    } else {
      // Hide posts that don't have corresponding data
      post.style.display = 'none';
    }
  });
  
  // If no cards match the search, show a message
  if (cards.length === 0) {
    const postsSection = document.getElementById('posts');
    const noResultsMessage = document.createElement('div');
    noResultsMessage.className = 'no-results-message';
    noResultsMessage.textContent = 'No cards found matching your search.';
    noResultsMessage.style.textAlign = 'center';
    noResultsMessage.style.padding = '20px';
    noResultsMessage.style.fontSize = '18px';
    noResultsMessage.style.color = '#666';
    
    // Check if the message already exists
    const existingMessage = postsSection.querySelector('.no-results-message');
    if (!existingMessage) {
      postsSection.appendChild(noResultsMessage);
    }
  } else {
    // Remove the no results message if it exists
    const existingMessage = document.querySelector('.no-results-message');
    if (existingMessage) {
      existingMessage.remove();
    }
  }
}
