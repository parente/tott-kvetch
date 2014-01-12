<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8"> 
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kvetch</title>
    <link rel="stylesheet" href="{{static_path}}/vendor/bootstrap/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{static_path}}/css/main.css">
    <script>var STATIC_PATH='{{static_path}}';</script>
  </head>
  <body>

    <div class="container">
      <div id="app" class="sheet">
        <div class="jumbotron">
          <h1>Kvetch</h1>
          <p>What really grinds your gears?</p>

          <div class="row input-row">
            <!-- input -->
            <div class="col-lg-12">
              <div class="input-group">
                <input id="input" type="text" class="form-control" maxlength="140">
                <span class="input-group-btn">
                  <button id="submit" class="btn btn-primary" type="button">Vent</button>
                </span>
              </div>
            </div>
          </div>
        </div>
    
        <div class="row posts-row">
          <div class="col-sm-6">
            <h2>Latest</h2>
            <div id="latest"></div>
          </div>
          <div class="col-sm-6">
            <h2>Favorites</h2>
            <div id="favorites"></div>
          </div>
        </div>          
      </div>
    </div>

    <script type="text/template" id="post-template">
      <div class="body"><%- attributes.body %></div>
      <div class="votes"><span class="count"><%- attributes.votes ? attributes.votes : '' %></span> <a class="upvote" href="javascript:">+1</a></div>
      <div class="timestamp"><%- attributes.timestamp ? new Date(attributes.timestamp).toLocaleString() : '' %>
      </div>
    </script>

    <script src="{{static_path}}/vendor/jquery/jquery.min.js"></script>
    <script src="{{static_path}}/vendor/underscore/underscore-min.js"></script>
    <script src="{{static_path}}/vendor/backbone/backbone-min.js"></script>
    <script src="{{static_path}}/js/models/post.js"></script>
    <script src="{{static_path}}/js/collections/posts.js"></script>
    <script src="{{static_path}}/js/views/post-view.js"></script>
    <script src="{{static_path}}/js/views/posts-view.js"></script>
    <script src="{{static_path}}/js/views/app-view.js"></script>
    <script src="{{static_path}}/js/main.js"></script>
  </body>
</html>
