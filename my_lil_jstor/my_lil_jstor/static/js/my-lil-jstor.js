// Please include or add javascript to this file
import $ from "jquery";

$('#like-link').on('click', function (event) {
  event.preventDefault();
  console.log("like-link clicked")
  const action = $('#like-link').text()
  if (action === 'Like')
    addLike()
  else
    subtractLike()
});

$('#leave-comment-button').on('click', function (event) {
  event.preventDefault();
  console.log("leave-comment-button clicked")
  const linkText = $('#leave-comment-button').text()
  console.log('leave-comment-button handler: linkText = ', linkText)
  // determine class of comment form, and use in IF statement
  const formClass = $('#comment-form').attr("class");
  if (formClass === '') {
    console.log('leave-comment-button handler: hiding form')
    $('#leave-comment-button').text('Leave a comment')
    $('#comment-form').attr('class', 'visuallyhidden')
  }
  else {
    console.log('leave-comment-button handler: showing form')
    $('#leave-comment-button').text('Hide comment form')
    $('#comment-form').attr('class', '')
  }
});


function addLike(elem) {
  event.preventDefault();

  console.log("addLike function: invoked") // sanity check
  console.log("addLike function: window.location.pathname = ", window.location.pathname)

  $.ajax({
    url: window.location.pathname + "/like",
    type: 'GET',
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    success: function (result) {
      console.log('ajax call was successful')
      console.log('ajax function: num_likes = ', result.num_likes)
      const book_id = window.location.pathname.split("/")[2]
      console.log('book_id = ', book_id)
      const markup = getLikesMarkup(result.num_likes, book_id)

      $('#like-link').text(markup.linkText)
      $('#like-link-msg').text(markup.linkMsg)
    },
    error: function () {
      console.log('ajax call error')
    }
  });
}

function subtractLike(elem) {

  console.log("subtractLike function: invoked") // sanity check
  console.log("subtractLike function: window.location.pathname = ", window.location.pathname)

  $.ajax({
    url: window.location.pathname + "/unlike",
    type: 'GET',
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    success: function (result) {
      console.log('ajax call was successful')
      console.log('ajax function: num_likes = ', result.num_likes)
      const book_id = window.location.pathname.split("/")[2]
      console.log('book_id = ', book_id)
      const markup = getLikesMarkup(result.num_likes, book_id)

      $('#like-link').text(markup.linkText)
      $('#like-link-msg').text(markup.linkMsg)
    },
    error: function () {
      console.log('ajax call error')
    }
  });
}

function getLikesMarkup(num_likes, book_id) {
  // get cookie likes_coloring_book_ for book_id
  const cookieName = 'likes_coloring_book_' + book_id
  const cookieVal = getCookie(cookieName)
  console.log('getLikesMarkup: cookieVal = ', cookieVal)
  const linkText = cookieVal ? 'Unlike' : 'Like'
  console.log('getLikesMarkup: linkText = ', linkText)
  let linkMsg = 'Be the first to like this'

  if (num_likes === 1) {
    if (cookieVal)
      linkMsg = 'You like this'
    else
      linkMsg = '1 person likes this'
  }
  else if (num_likes === 2) {
    if (cookieVal)
      linkMsg = 'You and 1 person likes this'
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
  console.log('getLikesMarkup: markup = ', markup)
  return markup
}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') c = c.substring(1);
    if (c.indexOf(name) != -1) return c.substring(name.length, c.length);
  }
  return "";
} 