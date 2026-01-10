function estimatePrice() {
  console.log("Estimate price button clicked");
  var sqft = $("#uiSqft").val();
  var bhk = $("input[name='uiBHK']:checked").val();
  var bath = $("input[name='uiBathrooms']:checked").val();
  var location = $("#uiLocations").val();
  var resultArea = $("#uiEstimatedPrice");

  // Show "Processing..." while waiting
  resultArea.html("<h3>Calculating...</h3>");

  $.post("/predict_home_price", {
      Squareft: parseFloat(sqft),
      uiBHK: bhk,
      uiBathrooms: bath,
      uiLocations: location
  }, function(data, status) {
      console.log(data.estimated_price);
      // Update result with the actual value
      resultArea.html("<h3>Estimated Price: ₹ " + data.estimated_price + " Lakh</h3>");
  }).fail(function() {
      resultArea.html("<h3 style='color:red;'>Error: Could not calculate price</h3>");
  });
}

$(document).ready(function () {
  console.log("Document ready");
  $.get("/get_location_names", function (data) {
    if(data && data.locations) {
      var uiLocations = $("#uiLocations");
      // uiLocations.empty(); // Optional: clears existing
      data.locations.forEach(function (location) {
        uiLocations.append(new Option(location, location));
      });
    }
  });
});