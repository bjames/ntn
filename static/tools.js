var static_count = 10
var variable_count = static_count
var timer = null
var curr_active = null
var paused = false

$(document).ready(function() {

    $('#bottom_buttons').css('display', 'inherit');
    $('#nojs_text').css('display', 'none');


    load_anchor();

    // handle watch already being set on a reload
    watch();

    $('#app').submit(function(event){

        event.preventDefault();
        submit_form();
    
    })

    $('#watch').click(function() {

        watch();

    })

    // navbar clicks are handled here
    $('#dns_nav').click(function(event){
        event.preventDefault(event);
        active(this);
        load_app('dns', 'DNS');
        enable_watch();
        response_navbar();
        return false;
    })
    $('#subnet_nav').click(function(event){
        event.preventDefault(event);
        active(this);
        load_app('subnet', 'Subnet');
        disable_watch();
        response_navbar();
        return false;
    })
    $('#curl_nav').click(function(event){
        event.preventDefault(event);
        active(this);
        load_app('curl', 'cURL');
        enable_watch();
        response_navbar();
        return false;
    })
    $('#oui_nav').click(function(event){
        event.preventDefault(event);
        active(this)
        load_app('oui', 'OUI');
        disable_watch();
        response_navbar();
        return false;
    })
    $('#ping_nav').click(function(event){
        event.preventDefault(event);
        active(this);
        load_app('ping', 'Ping');
        enable_watch();
        response_navbar();
        return false;
    })
    $('#traceroute_nav').click(function(event){
        event.preventDefault(event);
        active(this);
        load_app('traceroute', 'Traceroute');
        enable_watch();
        response_navbar();
        return false;
    })
    $('#whois_nav').click(function(event){
        event.preventDefault(event);
        active(this);
        load_app('whois', 'Whois');
        disable_watch();
        response_navbar();
        return false;
    })

    $('#rphash_nav').click(function(event){
        event.preventDefault(event);
        active(this);
        load_app('rphash', 'RPHash');
        disable_watch();
        response_navbar();
        return false;
    })
    
    $('#clear_scrollback').click(function(){
        $('#term').empty();
    })
    $('#nav_icon').click(function(){
        response_navbar();
    })
});

function disable_watch() {
    $('#watch').attr('disabled', true);
    $('#watch').attr('checked', false);
    $('#timer').css('visibility', 'hidden');
    clearInterval(timer);
}

function enable_watch() {
    $('#watch').attr('disabled', false)
}

function active(element) {

    if(curr_active != null){
        $(curr_active).attr('class', '');
    }
    curr_active = element
    $(element).attr('class', 'active');

}

function start_timer() {

    timer = setInterval(function() {
        countdown();
        $('#timer').css('visibility', 'visible');
    }, 1000)

}

// countdown timer for the watch function
function countdown(timer) {

    if (!paused) {

        variable_count = variable_count - 1;

        document.getElementById('timer').innerHTML=variable_count;

        if (variable_count == 0)
        {
            paused = true;
            submit_form();
            variable_count = static_count;
        }
    
    }

}

function watch() {

    var checked = $('#watch').is(':checked');

    if(checked) {
        variable_count = static_count;
        start_timer();
    }else{

        try {
            clearInterval(timer);
            $('#timer').css('visibility', 'hidden');
        }catch(e){
            // ignore errors due to unset timer here
        }

    }
}

// used to submit the app forms via ajax
function submit_form() {

    var curr_app = document.getElementById("app").firstChild;

    classes = curr_app.classList;

    // disable the submit button to show the user we are working on the request
    $('#submit_app').attr('disabled', true);
    $('#term').addClass('spinner');

    if(classes.contains("curl")){

        var url = $('[name=url]').val();
        var follow_redirects = $('[name=follow_redirects]').is(':checked');

        $.ajax({
            url: '/tools/curl',
            type: 'post',
            cache: false,
            data: {url: url, follow_redirects: follow_redirects},
            success: function(data) {
                set_location('/tools/curl?url=' + url + '&follow_redirects=' + follow_redirects);
                post_success(data);
            },
            error: function() {
                post_failed();
            }
        });

    }else if (classes.contains("dns")){

        var url = $('[name=url]').val();
        var record_type = $('[name=record_type]').val();
        var user_resolver = $('[name=user_resolver]').val();

        $.ajax({
            url: '/tools/dns',
            type: 'post',
            cache: false,
            data: {url: url, record_type: record_type, user_resolver: user_resolver},
            success: function(data) {

                set_location('/tools/dns?url=' + url + '&record_type=' + record_type + '&user_resolver=' + user_resolver);
                post_success(data);

            },
            error: function() {
                post_failed();
            }
        });

    }else if (classes.contains("subnet")){

        var ip_address = $('[name=ip_address]').val();
        var subnet_mask = $('[name=subnet_mask]').val();

        $.ajax({
            url: '/tools/subnet',
            type: 'post',
            cache: false,
            data: {ip_address: ip_address, subnet_mask: subnet_mask},
            success: function(data) {

                set_location('/tools/subnet?ip_address=' + ip_address + '&subnet_mask=' + subnet_mask);
                post_success(data);
            
            },
            error: function() {
                post_failed();
            }
        });

    }else if (classes.contains("oui")){

        var mac_address = $('[name=mac_address]').val();

        $.ajax({
            url: '/tools/oui',
            type: 'post',
            cache: false,
            data: {mac_address: mac_address},
            success: function(data) {

                set_location('/tools/oui?mac_address=' + mac_address);
                post_success(data);
            
            },
            error: function() {
                post_failed();
            }
        });

    }else if (classes.contains("ping")){

        var hostname = $('[name=hostname]').val();

        $.ajax({
            url: '/tools/ping',
            type: 'post',
            cache: false,
            data: {hostname: hostname},
            success: function(data) {

                set_location('/tools/ping?hostname=' + hostname);
                post_success(data);
            
            },
            error: function() {
                post_failed()
            }
        });

    }else if (classes.contains("traceroute")){

        var hostname = $('[name=hostname]').val();

        $.ajax({
            url: '/tools/traceroute',
            type: 'post',
            cache: false,
            data: {hostname: hostname},
            success: function(data) {

                set_location('/tools/traceroute?hostname=' + hostname);
                post_success(data);
            
            },
            error: function() {
                post_failed();
            }
        });
    }else if (classes.contains("whois")){

        var hostname = $('[name=hostname]').val();

        $.ajax({
            url: '/tools/whois',
            type: 'post',
            cache: false,
            data: {hostname: hostname},
            success: function(data) {

                set_location('/tools/whois?hostname=' + hostname);
                post_success(data);
            
            },
            error: function() {
                post_failed();
            }
        });
    }else if (classes.contains("rphash")){

        var rp_address = $('[name=rp_address]').val();
        var group = $('[name=group]').val();
        var mask = $('[name=mask]').val();

        $.ajax({
            url: '/tools/rphash',
            type: 'post',
            cache: false,
            data: {rp_address: rp_address, group: group, mask: mask},
            success: function(data) {

                set_location('/tools/rphash?rp_address=' + rp_address + '&group=' + group + '&mask=' + mask);
                post_success(data);
            
            },
            error: function() {
                post_failed();
            }
        });
    }
}

function post_success(data) {
    update_term(data);  
    paused = false;
    $('#submit_app').attr('disabled', false);
    $('#term').removeClass('spinner');
}

function post_failed() {
    paused = false;
    $('#submit_app').attr('disabled', false);
    $('#term').removeClass('spinner');
}

// used to append data to the terminal
function update_term(term_data) {

    $("#term").append(term_data);

    var term = document.getElementById("term");
    term.scrollTop = term.scrollHeight;
}

// loads the form above the terminal box
function load_app(app, title) {
    $('#app').load('/tools/'+ app + ' #app');
    active($('#' + app + '_nav'));
    document.title = 'NTN - '+ title;
    set_location('/tools/' + app)
}

// allows bookmarks to function - if the request URL is #app, the app is loaded
function load_anchor() {

    switch ($(location).attr('pathname')) {
        case '/tools/curl':
            enable_watch();
            active($('#curl_nav'));
            return;
        case '/tools/dns':
            enable_watch();
            active($('#dns_nav'));
            return;
        case '/tools/ping':
            enable_watch();
            active($('#ping_nav'));
            return;
        case '/tools/oui':
            active($('#oui_nav'));
            return;
        case '/tools/subnet':
            active($('#subnet_nav'));
            return;
        case '/tools/traceroute':
            enable_watch();
            active($('#traceroute_nav'));
            return;
        case '/tools/whois':
            active($('#whois_nav'));
            return;
        case '/tools/rphash':
            active($('#rphash_nav'));
            return;
    }
}

function response_navbar() {
    var element = document.getElementById("tools_nav");
    if (element.className === "tools_nav") {
        element.className += " responsive";
    } else {
        element.className = "tools_nav";
    }
} 

function set_location(url_location) {
    window.history.pushState(null, null, url_location)
}