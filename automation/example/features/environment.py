import tagui as t
def before_all(context):
    t.init(visual_automation=True, chrome_browser=True)
def after_all(context):
    t.close()