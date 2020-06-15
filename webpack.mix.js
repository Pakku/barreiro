let mix = require('laravel-mix');


mix.setPublicPath('blog')
   .js('blog/resources/js/app.js', 'blog/static/blog/js')
   .sass('blog/resources/scss/app.scss', 'blog/static/blog/css')
    .options({
        processCssUrls: false
    })
;