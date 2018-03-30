//初始化加载
$(function () {
    // $('.article_body').load('/static/my/page/article.html')
    $('.url_param_group').attr('href', '/?param_group=' + $('.url_param_group').text())
    $('.url_param_date').attr('href', '/?param_date=' + $('.url_param_date').text())
});
