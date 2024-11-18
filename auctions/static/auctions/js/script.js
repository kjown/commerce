document.addEventListener("DOMContentLoaded", function() {
    // Close Auction Confirmation Dialog
    const closeAuctionButton = document.querySelector("#close-auction-btn");
    closeAuctionButton.addEventListener("click", function(event) {
        const confirmed = confirm("Are you sure you want to close this listing?");
        if (!confirmed) {
            event.preventDefault();
        }
    });

    // Add to Watchlist alert
    const addToWatchlist = document.querySelector("#add-watchlist-btn");
    addToWatchlist.addEventListener("click", function() {
        alert("Listing added to watchlist.")
    });

    // Add to Watchlist alert
    const removeFromWatchlist = document.querySelector("#remove-watchlist-btn");
    removeFromWatchlist.addEventListener("click", function() {
        alert("Listing removed from watchlist.");
    });

    // Format pricing format for all bidAmount elements
    const bidElements = document.querySelectorAll(".bidAmount");
    bidElements.forEach(function(bidElement) {
        const bidValue = parseFloat(bidElement.textContent.replace('RM', '').trim());
        if (!isNaN(bidValue)) {
            bidElement.textContent = `RM ${bidValue.toLocaleString()}`;
        }
    });
})