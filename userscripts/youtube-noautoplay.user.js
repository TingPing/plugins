// ==UserScript==
// @name        Youtube No Autoplay
// @namespace   se.tingping
// @description Disables auto-play on playlists by default
// @include     /^https?://(www\.)?youtube\.com//
// @version     1
// @grant       none
// ==/UserScript==

var header = document.getElementById('watch-appbar-playlist');
if (header)
{
  var headers = header.getElementsByClassName('playlist-header-content');
  headers[0].setAttribute('data-initial-autoplay-state', 'false');

  // Now it's disabled but looks enabled still
  // FIXME: This still doesn't immediately update the icon though
  var controls = document.getElementsByClassName('playlist-nav-controls')[0];
  if (controls)
  {
    // Just assume it's the first button
    var button = controls.getElementsByTagName('button')[0];
    button.setAttribute('data-button-toggle', 'false');
  }
}
