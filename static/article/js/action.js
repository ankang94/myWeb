//回到顶部
$(window).scroll(function () {
    $('#to-top').hide();
    if ($(window).scrollTop() >= 600) {
        $('#to-top').show();
    }
});
$(function () {
    // 目录与内容判断
    var navigationBar = $('.cl-nav-bar'),
        navigationFooter = $('.footer'),
        catlogFlag = $('.wrapper-catlog').length > 0,
        navigationContent = catlogFlag ? $('.wrapper-catlog') : $('.wrapper-content');


    //bootstrap4 tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // right-bar margin
    $('.right-bar:first').children('div').not(':first').css('margin', '5px 0');

    $("#to-top").on('click', function () {
        var speed = 400;//滑动的速度
        $('body,html').animate({scrollTop: 0}, speed);
        return false;
    });

    /* --------------------------------

     1. Footer

     -------------------------------- */
    setTimeout(function () {
        positionFooter();

        function positionFooter() {
            // A4 size
            if ((navigationBar.height() + navigationContent.height() + navigationFooter.height()) < navigationContent.width() * 1.5) {
                navigationContent.height(navigationContent.width() * 1.5);
            }
            if ($('.catlog-grid').height() > navigationContent.width() * 1.5 || innerWidth < 450) {
                $('#pagebar').css('position', 'static');
            }
            // 屏蔽反色闪屏
            navigationFooter.css('display', 'block');
            $('#pagebar').css('display', 'block');
        }

        $(window).scroll(positionFooter).resize(positionFooter);
    }, 100);

    /* --------------------------------

     2. Float-Nav-Bar

     -------------------------------- */
    //set scrolling variables
    var scrolling = false,
        previousTop = 0,
        scrollDelta = 10;


    $(window).on('scroll', function () {
        if (!scrolling) {
            scrolling = true;
            (!window.requestAnimationFrame) ?
                setTimeout(autoHideHeader, 250) : requestAnimationFrame(autoHideHeader);
        }
    });

    function autoHideHeader() {
        var currentTop = $(window).scrollTop();
        checkStickyNavigation(currentTop);
        previousTop = currentTop;
        scrolling = false;
    }

    function checkStickyNavigation(currentTop) {
        //secondary nav below intro section - sticky secondary nav
        var navOffsetTop = navigationContent.offset().top - navigationBar.outerHeight();

        if (previousTop >= currentTop) {
            //向上滚动
            if (currentTop < navOffsetTop) {
                catlogFlag ? null:navigationBar.removeClass('is-hidden');
                navigationContent.removeClass('wrapper-slide');
                navigationBar.removeClass('fixed');
            } else if (previousTop - currentTop > scrollDelta) {
                catlogFlag ? null:navigationBar.removeClass('is-hidden');
                navigationContent.addClass('wrapper-slide');
                navigationBar.addClass('fixed');
            }

        } else {
            //向下滚动
            if (currentTop > navOffsetTop) {
                catlogFlag ? null:navigationBar.addClass('is-hidden');
                navigationBar.addClass('fixed');
                navigationContent.addClass('wrapper-slide');
            }
        }
    }

    /* --------------------------------

     3. Line-To-Line-Cav

     -------------------------------- */

    //封装方法，压缩之后减少文件大小
    function get_attribute(node, attr, default_value) {
        return node.getAttribute(attr) || default_value;
    }

    //封装方法，压缩之后减少文件大小
    function get_by_tagname(name) {
        return document.getElementsByTagName(name);
    }

    //彩色线条
    function default_color() {
        // return '#'+('00000'+(Math.random()*0x1000000<<0).toString(16)).slice(-6);
        return Math.ceil(Math.random() * 255) + ',' + Math.ceil(Math.random() * 255) + ',' + Math.ceil(Math.random() * 255);
    }

    //获取配置参数
    function get_config_option() {
        var scripts = get_by_tagname("script"),
            script_len = scripts.length,
            script = scripts[script_len - 1]; //当前加载的script
        return {
            l: script_len, //长度，用于生成id用
            z: get_attribute(script, "zIndex", -1), //z-index
            o: get_attribute(script, "opacity", 0.5), //opacity
            c: get_attribute(script, "color", default_color()), //color
            n: get_attribute(script, "count", 99) //count
        };
    }

    //设置canvas的高宽
    function set_canvas_size() {
        canvas_width = the_canvas.width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth,
            canvas_height = the_canvas.height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
    }

    //绘制过程
    function draw_canvas() {
        context.clearRect(0, 0, canvas_width, canvas_height);
        //随机的线条和当前位置联合数组
        var e, i, d, x_dist, y_dist, dist; //临时节点
        //遍历处理每一个点
        random_points.forEach(function (r, idx) {
            r.x += r.xa,
                r.y += r.ya, //移动
                r.xa *= r.x > canvas_width || r.x < 0 ? -1 : 1,
                r.ya *= r.y > canvas_height || r.y < 0 ? -1 : 1, //碰到边界，反向反弹
                context.fillRect(r.x - 0.5, r.y - 0.5, 1, 1); //绘制一个宽高为1的点
            //从下一个点开始
            for (i = idx + 1; i < all_array.length; i++) {
                e = all_array[i];
                // 当前点存在
                if (null !== e.x && null !== e.y) {
                    x_dist = r.x - e.x; //x轴距离 l
                    y_dist = r.y - e.y; //y轴距离 n
                    dist = x_dist * x_dist + y_dist * y_dist; //总距离, m

                    dist < e.max && (e === current_point && dist >= e.max / 2 && (r.x -= 0.03 * x_dist, r.y -= 0.03 * y_dist), //靠近的时候加速
                        d = (e.max - dist) / e.max,
                        context.beginPath(),
                        context.lineWidth = d,
                        context.strokeStyle = "rgba(" + config.c + "," + (d + 0.2) + ")",
                        context.moveTo(r.x, r.y),
                        context.lineTo(e.x, e.y),
                        context.stroke());
                }
            }
        }), frame_func(draw_canvas);
    }

    //创建画布，并添加到body中
    var the_canvas = document.createElement("canvas"), //画布
        config = get_config_option(), //配置
        canvas_id = "c_n" + config.l, //canvas id
        context = the_canvas.getContext("2d"), canvas_width, canvas_height,
        frame_func = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame || function (func) {
                window.setTimeout(func, 1000 / 60);
            }, random = Math.random,
        current_point = {
            x: null, //当前鼠标x
            y: null, //当前鼠标y
            max: 20000 // 圈半径的平方
        },
        all_array;
    the_canvas.id = canvas_id;
    the_canvas.style.cssText = "position:fixed;top:0;left:0;z-index:" + config.z + ";opacity:" + config.o;
    get_by_tagname("body")[0].appendChild(the_canvas);

    //初始化画布大小
    set_canvas_size();
    window.onresize = set_canvas_size;
    //当时鼠标位置存储，离开的时候，释放当前位置信息
    window.onmousemove = function (e) {
        e = e || window.event;
        current_point.x = e.clientX;
        current_point.y = e.clientY;
    }, window.onmouseout = function () {
        current_point.x = null;
        current_point.y = null;
    };
    //随机生成config.n条线位置信息
    for (var random_points = [], i = 0; config.n > i; i++) {
        var x = random() * canvas_width, //随机位置
            y = random() * canvas_height,
            xa = 2 * random() - 1, //随机运动方向
            ya = 2 * random() - 1;
        // 随机点
        random_points.push({
            x: x,
            y: y,
            xa: xa,
            ya: ya,
            max: 6000 //沾附距离
        });
    }
    all_array = random_points.concat([current_point]);
    //0.1秒后绘制
    setTimeout(function () {
        frame_func(draw_canvas);
    }, 100);

    /* --------------------------------

     4. Color-Tags

     -------------------------------- */
    var colorpool = {};
    var colorbang = ['#78BBE6', '#EFE909', '#A3DE83', '#00BBF0', '#FF2E63', '#0D7377', '#AC005D', '#0881A3', '#EDA045']


    $('.tags_group').find('label').each(function () {
        if (colorpool[$(this).children('abbr').get(0).innerHTML]) {
            $(this).css('background', colorpool[$(this).children('abbr').get(0).innerHTML]);
        } else {
            if (colorbang.length > 0) {
                $(this).css('background', colorbang.pop());
            }
            colorpool[$(this).children('abbr').get(0).innerHTML] = $(this).css('background');
        }
    });
});