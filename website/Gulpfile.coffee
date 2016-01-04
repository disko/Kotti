gulp = require 'gulp'

coffee = require 'gulp-coffee'
concat = require 'gulp-concat'
cssmin = require 'gulp-cssmin'
rename = require 'gulp-rename'
sass = require 'gulp-sass'
uglify = require 'gulp-uglify'


paths =
  src:
    js:
      vendor: [
        './node_modules/jquery/dist/jquery.js',
        './node_modules/bootstrap/dist/js/bootstrap.js'
      ]
    sass: './styles/kotti.scss'

  dest:
    js: './assets/static/js'
    css: './assets/static/css'
    fonts: './assets/static/fonts'

gulp.task 'fonts', ->
  gulp.src "./node_modules/font-awesome/fonts/*"
    .pipe gulp.dest(paths.dest.fonts)

gulp.task 'js-vendor', ->
  gulp.src paths.src.js.vendor
    .pipe concat('vendor.js')
    .pipe gulp.dest(paths.dest.js)
    .pipe uglify()
    .pipe rename(suffix: '.min')
    .pipe gulp.dest(paths.dest.js)


gulp.task 'sass', ->
  gulp.src paths.src.sass
    .pipe sass()
    .pipe gulp.dest(paths.dest.css)
    .pipe cssmin()
    .pipe rename(suffix: '.min')
    .pipe gulp.dest(paths.dest.css)

gulp.task 'watch', ->
  gulp.watch paths.src.sass, ['sass']
  gulp.watch paths.src.js.vendor, ['js-vendor']

gulp.task 'default', [
  'js-vendor',
  'fonts',
  'sass',
  'watch'
]
