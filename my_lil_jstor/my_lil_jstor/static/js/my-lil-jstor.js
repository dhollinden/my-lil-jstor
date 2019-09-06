// Please include or add javascript to this file
import $ from 'jquery';

// toggles visibility of the comment form
$('#leave-comment-link').on('click', function (event) {
  event.preventDefault();
  const formClass = $('#comment-form').attr('class');
  if (formClass === '') {
    $('#leave-comment-link').text('Leave a comment')
    $('#comment-form').attr('class', 'visuallyhidden')
  }
  else {
    $('#leave-comment-link').text('Hide comment form')
    $('#comment-form').attr('class', '')
  }
});


// toggles Likes link text and message, updates discounted price
$('#like-link').on('click', function (event) {
  event.preventDefault();
  const action = $('#like-link').text().toLowerCase()
  console.log('like-link clicked: ', action)
  $.ajax({
    url: window.location.pathname + '/' + action,
    type: 'GET',
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    success: function (result) {
      console.log('ajax call success: num_likes =', result.num_likes, ',discounted_price =', result.discounted_price)
      const book_id = window.location.pathname.split('/')[2]
      const markup = getLikesMarkup(result.num_likes, book_id)
      $('#like-link').text(markup.linkText)
      $('#like-link-msg').text(markup.linkMsg)
      $('#price').text(result.discounted_price)
    },
    error: function () {
      console.log('ajax call error')
    }
  });
});


// generates Likes message based on number of likes and cookie
function getLikesMarkup(num_likes, book_id) {
  const cookieVal = getCookie('likes_coloring_book_' + book_id)
  const linkText = cookieVal ? 'Unlike' : 'Like'

  let linkMsg = 'Be the first to like this'

  if (num_likes === 1) {
    if (cookieVal)
      linkMsg = 'You like this'
    else
      linkMsg = '1 person likes this'
  }
  else if (num_likes === 2) {
    if (cookieVal)
      linkMsg = 'You and 1 person like this'
    else
      linkMsg = '2 people like this'
  }
  else if (num_likes > 2) {
    if (cookieVal)
      linkMsg = 'You and ' + String(num_likes - 1) + ' people like this'
    else
      linkMsg = String(num_likes) + ' people like this'
  }

  const markup = {
    linkText: linkText,
    linkMsg: linkMsg
  }
  console.log('getLikesMarkup: cookieVal = ', cookieVal)
  console.log('getLikesMarkup: markup = ', markup)
  return markup
}

function getCookie(cname) {
  const name = cname + '=';
  const ca = document.cookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') c = c.substring(1);
    if (c.indexOf(name) != -1) return c.substring(name.length, c.length);
  }
  return '';
} 