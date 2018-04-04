$(function () {
    var urlstr = window.location.pathname;
    var param = urlstr.match(/a\/(\d+)/g) + ''
    var aid = param.split('\/')[1]

    $('.article_content').find('img')
});
