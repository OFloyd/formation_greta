/**
 * @license
 * Copyright 2019 Google LLC. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

// Initialize and add the map
function initMap(): void {
  // The location of Uluru
  const paris = { lat: 48.8, lng: 2.3 };
  // The map, centered at Uluru
  const map = new google.maps.Map(
    document.getElementById("map") as HTMLElement,
    {
      zoom: 11,
      center: paris,
    }
  );

  // The marker, positioned at Uluru
  const marker = new google.maps.Marker({
    position: paris,
    map: map,
  });
}

declare global {
  interface Window {
    initMap: () => void;
  }
}
window.initMap = initMap;
export {};
