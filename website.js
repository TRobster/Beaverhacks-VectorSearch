// Load the cards data when the page loads
document.addEventListener('DOMContentLoaded', () => {
  // Fetch the cards data
  fetch('cards.json')
    .then(response => response.json())
    .then(cards => {
      // Store the cards data for later use
      window.cardsData = cards;
      
      // Display all cards initially
      displayCards(cards);
      
      // Add event listener to the search input
      const searchInput = document.getElementById('filter-text');
      searchInput.addEventListener('input', () => {
        const searchTerm = searchInput.value.toLowerCase();
        const filteredCards = filterCards(cards, searchTerm);
        displayCards(filteredCards);
      });
      
      // Add event listener to the update button
      const updateButton = document.getElementById('filter-update-button');
      updateButton.addEventListener('click', () => {
        const searchTerm = searchInput.value.toLowerCase();
        const filteredCards = filterCards(cards, searchTerm);
        displayCards(filteredCards);
      });
    })
    .catch(error => console.error('Error loading cards data:', error));
});

// Function to filter cards based on search term
function filterCards(cards, searchTerm) {
  if (!searchTerm) return cards;
  
  return cards.filter(card => 
    card.title.toLowerCase().includes(searchTerm)
  );
}

// Function to display cards in the posts section
function displayCards(cards) {
  const postsSection = document.getElementById('posts');
  const posts = postsSection.querySelectorAll('.post');
  
  // Clear existing posts
  postsSection.innerHTML = '';
  
  // If no cards match the search, show a message
  if (cards.length === 0) {
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
  cards.forEach(card => {
    const postElement = document.createElement('div');
    postElement.className = 'post';
    postElement.innerHTML = `
      <div class="post-contents">
        <div class="post-image-container">
          <img src="${card.imageUrl}" alt="${card.title}">
        </div>
        <div class="post-info-container">
          <a href="#" class="post-title">${card.title}</a>
        </div>
      </div>
    `;
    postsSection.appendChild(postElement);
  });
}
