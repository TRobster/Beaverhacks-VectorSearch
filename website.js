// Global variable to store card data
let cardData = [];
let filteredCardData = [];

// Load card data when the page loads
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const response = await fetch('cardData.json');
    cardData = await response.json();
    filteredCardData = [...cardData]; // Initialize filtered data with all cards
    console.log('Card data loaded:', cardData);
    
    // Set up search input event listener
    const searchInput = document.getElementById('filter-text');
    if (searchInput) {
      searchInput.addEventListener('input', handleSearch);
    }
    
    // Initial display of cards
    updateImages();
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
  updateImages();
}

const button = document.getElementById("filter-update-button");
button.addEventListener("click", updateImages);

function updateImages() {
  console.log("Updating images with card data");
  
  // Get all post elements
  const posts = document.querySelectorAll('.post');
  
  // Update each post with data from the JSON
  posts.forEach((post, index) => {
    if (index < filteredCardData.length) {
      // Get the image and title elements
      
      const imgElement = post.querySelector('#dynamicImage');
      const titleElement = post.querySelector('.post-title');
      
      // Update the image source and title
      if (imgElement) {
        imgElement.src = filteredCardData[index].imageUrl;
        imgElement.alt = filteredCardData[index].title;
      }
      
      if (titleElement) {
        titleElement.textContent = filteredCardData[index].title;
      }
      
      // Show the post
      post.style.display = 'block';
    } else {
      // Hide posts that don't have corresponding data
      post.style.display = 'none';
    }
  });
}

 
