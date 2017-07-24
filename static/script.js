// AJAX calls

function openBrowser(url, destination, password){
  var jqXHR = $.ajax({
    type: "POST",
    url: "/openBrowser",
    async: true,
    data: {
      url: url,
      destination: destination,
      password: password }
  });
  return jqXHR.responseText;
}

// Helper functions

function changeBackground(){
  pic_num = Math.floor((Math.random() * 10) + 1);
  $('#landscape').attr('src', 'static/landscape/landscape_' + pic_num + '.jpg');
}

function loadShowDetails(){
  var tv_show_names = ["12 Monkeys","Billions","Black Mirror","Fear the Walking Dead","Game of Thrones","Homeland","Suits","Stranger Things","The Walking Dead","Zoo"]

  for (var i=0; i< tv_show_names.length; i++) {
    var tvURL = "http://api.tvmaze.com/search/shows?q=" + tv_show_names[i];
    var episodeURL = "";
    console.log(tv_show_names[i]);

    //Get ratings and next episode url
    var showResponse = $.ajax({
        url:tvURL,
        dataType: "json",
        async: false,
        success: function(response) {
          return response[0];
        }
    });

    showResponse = showResponse.responseJSON[0];
    $('#tvShowRatingsTable').append('<tr><td></td><td><a href="http://www.imdb.com/title/' + showResponse.show.externals.imdb + '" target="_blank">' + showResponse.show.name + '</a></td><td class="text-center">' + showResponse.show.rating.average + '</td></tr>');
    //Check that next episode url exists
    try {
      episodeURL = showResponse.show._links.nextepisode.href;
    }
    catch(err) {
    };

    //Get season, episode number and airdate for next episode
    if (episodeURL) {
      episodeResponse = $.ajax({
          url:episodeURL,
          dataType: "json",
          async: false,
          success: function(response) {
            return response;
          }
      });
      episodeResponse = episodeResponse.responseJSON;
      $('#tvShowNextEpisodeTable').append('<tr><td></td><td>' + tv_show_names[i] + ' [' + episodeResponse.season + 'x' + episodeResponse.number + ']</td><td class="text-center">' + episodeResponse.airdate + '</td></tr>');
    }
  }
}


// Click on icons

$("#landscape").on("click", function (e) {
  changeBackground();
});

$("#maybank").on("click", function (e) {
  var password = $('#password').val();
  if (password == "") {
    $('#error_message').text("Please key in password");
  }
  else {
    $('#error_message').text("");
    openBrowser("https://www.maybank2u.com.my/mbb/m2u/common/M2ULogin.do?action=Login", "Maybank", password);
  }
});

$("#publicbank").on("click", function (e) {
  var password = $('#password').val();
  if (password == "") {
    $('#error_message').text("Please key in password");
  }
  else {
    $('#error_message').text("");
    openBrowser("https://www2.pbebank.com/myIBK/apppbb/servlet/BxxxServlet?RDOName=BxxxAuth&MethodName=login", "Public Bank", password);
  }
});

$("#citibank").on("click", function (e) {
  var password = $('#password').val();
  if (password == "") {
    $('#error_message').text("Please key in password");
  }
  else {
    $('#error_message').text("");
    openBrowser("https://www.citibank.com.my/MYGCB/JSO/signon/DisplayUsernameSignon.do", "Citibank", password);
  }
});

$("#uob").on("click", function (e) {
  var password = $('#password').val();
  if (password == "") {
    $('#error_message').text("Please key in password");
  }
  else {
    $('#error_message').text("");
    openBrowser("https://pib.uob.com.sg/PIBLogin/Public/processPreCapture.do?keyId=lpc", "UOB", password);
  }
});

$("#publicmutual").on("click", function (e) {
  var password = $('#password').val();
  if (password == "") {
    $('#error_message').text("Please key in password");
  }
  else {
    $('#error_message').text("");
    openBrowser("https://www.publicmutualonline.com.my/pmblogin.aspx", "Public Mutual", password);
  }
});

$("#epf").on("click", function (e) {
  var password = $('#password').val();
  if (password == "") {
    $('#error_message').text("Please key in password");
  }
  else {
    $('#error_message').text("");
    openBrowser("https://secure.kwsp.gov.my/secured/member/login", "EPF", password);
  }
});

$("#sspni").on("click", function (e) {
  var password = $('#password').val();
  if (password == "") {
    $('#error_message').text("Please key in password");
  }
  else {
    $('#error_message').text("");
    openBrowser("https://www.ptptn.gov.my/saving/sspnlogin.html", "SSPN-i", password);
  }
});

$("#tnb").on("click", function (e) {
  var password = $('#password').val();
  if (password == "") {
    $('#error_message').text("Please key in password");
  }
  else {
    $('#error_message').text("");
    openBrowser("https://www.mytnb.com.my/", "TNB", password);
  }
});

$("#indahwater").on("click", function (e) {
  var password = $('#password').val();
  if (password == "") {
    $('#error_message').text("Please key in password");
  }
  else {
    $('#error_message').text("");
    openBrowser("https://www.iwk.com.my/customer/account-balance", "Indah Water", password);
  }
});

$("#time").on("click", function (e) {
  var password = $('#password').val();
  if (password == "") {
    $('#error_message').text("Please key in password");
  }
  else {
    $('#error_message').text("");
    openBrowser("https://selfcare.time.com.my/auth/login", "Time", password);
  }
});

// Runs these functions when webpage is loaded

$(document).ready(function(){
  loadShowDetails();
  var refreshId = setInterval( function()
   {
       changeBackground();
   }, 10000);
});
