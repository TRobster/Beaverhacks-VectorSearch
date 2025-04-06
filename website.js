let cardData = [];

// Load card data when the page loads
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const response = await fetch('cardData.json');
    cardData = await response.json();
    console.log('Card data loaded:', cardData);
  } catch (error) {
    console.error('Error loading card data:', error);
  }
});

const button = document.getElementById("filter-update-button");
button.addEventListener("click", updateImages);

function updateImages() {
  console.log("Updating images with card data");
  
  // Get all post elements
  const posts = document.querySelectorAll('.post');
  
  // Update each post with data from the JSON
  posts.forEach((post, index) => {
    if (index < cardData.length) {
      // Get the image and title elements
      const imgElement = post.querySelector('img');
      const titleElement = post.querySelector('.post-title');
      
      // Update the image source and title
      if (imgElement) {
        imgElement.src = cardData[index].imageUrl;
        imgElement.alt = cardData[index].title;
      }
      
      if (titleElement) {
        titleElement.textContent = cardData[index].title;
      }
    }
  });
}








