A basic web server that is able to render HTML and plain text with status codes. 

# Information

Hello! Thanks for coming to view this repoistory! It is currently under heavy development so please, expect bugs.

Curent bugs (Tick means bug is fixed):
- [ ] CTRL + C Does not end the program
- [ ] Random line added to text based responses

You may find examples of how to use this module in the examples folder.

# Whats new?

Here will be a list of a few updates from the past week or so.

14/05/24:

- A before request function has been added to run code before a request. For example, printing a successful connection.
- Allow collection of the request IP (May not work as intended if the webserver is behind a reverse proxy like nginx/apache and cloudflare), the request path for example `/this_is_a_path` and the response method.
