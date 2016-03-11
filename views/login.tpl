% rebase('base.tpl', title='Login')
	  %if login == 'failure':
	  <div class="alert alert-danger" role="alert">
        <strong>Login failed.</strong> Training not found or password wrong.
      </div>
	  %elif login == 'loggedout':
	  <div class="alert alert-warning" role="alert">
        <strong>Logged out.</strong> You have been logged out.
      </div>
	  %end
	  <form action='/login' method='post' class="form-signin">
        <h2 class="form-signin-heading">Login</h2>
        <label for="inputTraining" class="sr-only">Training</label>
        <input name="training" type="text" id="inputTraining" class="form-control" placeholder="Training" required autofocus>
        <label for="inputPassword" class="sr-only">Password</label>
        <input name="password" type="password" id="inputPassword" class="form-control" placeholder="Password" required>
        <label for="inputID" class="sr-only">CCO ID</label>
        <input name="username" type="text" id="inputID" class="form-control" placeholder="CCO ID" required>
        <button class="btn btn-lg btn-primary btn-block" type="submit" >Sign in</button>
      </form>