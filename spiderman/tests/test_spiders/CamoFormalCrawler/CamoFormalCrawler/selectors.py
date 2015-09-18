__author__ = 'Mohammed Hamdy'

camoformal_selectors = {
  "title":".product-name h2::text",
  "sizes":"tr:nth-child(4) option:nth-child(n+2)::text",
  "image_urls":".lightbox.zoom-thumbnail::attr(href), .zoom-image::attr(src)",
}