import os

SCRIPT_PATH = f"{os.path.split(os.path.abspath(__file__))[0]}"
COPYRIGHT_OWNER = "Brandon James"
RENDERER_CONFIG = {
    "input_directory": f"{SCRIPT_PATH}/raw/",
    "input_file_extensions": (".md", ".markdown"),
    "image_file_extensions": (".jpg", ".jpeg", ".png", ".svg"),
    "output_directory": f"{SCRIPT_PATH}/static/rendered/",
    "image_directory": f"{SCRIPT_PATH}/static/images/post/",
    "pandoc_extra_args": [],
}
NOTES_DIR = "notes"
SITE_NAME = "It's Never The Network"
HEADER_TEXT = "It's Never The Network"
DEFAULT_META_DESCRIPTION = "It's Never The Network! Technical deep dives, network tools and more!"
HEADER_IMAGE = "ntn.png"
NAV_LINKS = [
    ["/", "Home"],
    ["/tools", "Tools"],
    ["/about", "About"],
]
STYLESHEET = "notes-core.css"
URI = "neverthenetwork.com"
PANDOC_PATH = "/usr/bin/pandoc"
PRODUCTION = True
CUSTOM_HEAD_HTML = '''
<script id="mcjs">!function(c,h,i,m,p){m=c.createElement(h),p=c.getElementsByTagName(h)[0],m.async=1,m.src=i,p.parentNode.insertBefore(m,p)}(document,"script","https://chimpstatic.com/mcjs-connected/js/users/6be7bf8229e7c71c33fa5f465/621303c5cb9820f7968d8ebcf.js");</script>
<script async defer data-domain="neverthenetwork.com" src="https://plausible.io/js/plausible.js"></script>
'''
CUSTOM_FOOTER_HTML = '''
    <p>If this page has been useful, consider making a <a href="https://www.buymeacoffee.com/gTmjV6SfU" target="_blank">small donation</a> or subscribing to our mailing list</p>
    <!-- Begin Mailchimp Signup Form -->
    <div id="mc_embed_signup">
        <form action="https://brandonsjames.us3.list-manage.com/subscribe/post?u=6be7bf8229e7c71c33fa5f465&amp;id=b13b916ed0" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank" novalidate>
            <div id="mc_embed_signup_scroll">
            
            <input type="email" value="" name="EMAIL" class="email" id="mce-EMAIL" placeholder="email address" required>
            <!-- real people should not fill this in and expect good things - do not remove this or risk form bot signups-->
            <div style="position: absolute; left: -5000px;" aria-hidden="true"><input type="text" name="b_6be7bf8229e7c71c33fa5f465_b13b916ed0" tabindex="-1" value=""></div>
            <input type="submit" value="Subscribe" name="subscribe" id="mc-embedded-subscribe" class="button">
            </div>
        </form>
    </div>
    <!--End mc_embed_signup-->
'''