<!doctype html>
<html>
  <head>
    <title>{title} &ndash; {s_title}</title>
    <link rel="stylesheet" href="{baseurl}{basepath}_css/reset.css" />
    <link rel="stylesheet" href="{baseurl}{basepath}_css/layout.css" />
  </head>
  <body>
    <header>
      <a href="{baseurl}{basepath}">{s_title}</a>
      <span>{description}</span>
    </header>
    <article>
      <div class="meta">
        <h1>{title}</h1>
        <time datetime="{datetime}">{datetime}</span>
      </div>
      <div class="text">
        {content}
      </div>
    </article>
    <footer>
      <h1>&copy; {footer_year} <strong>{s_title}</strong></h1>
      {footer}
    </footer>
  </body>
</html>
