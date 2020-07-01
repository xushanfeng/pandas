PAGE_LIMIT = 10
SEX = {
    "男": 1,
    "女": 2
}

UNIT = {
    "米": 1,
    "支": 2,
    "个": 3
}

CLOSE_WIN = '''
<script>
    setTimeout(function(){
        parent.location.reload(true);
        var index = parent.layer.getFrameIndex(window.name);
        parent.layer.close(index);
    },3);
</script>
'''

REFRESH_PARENT_PAGE = '''
<script>
        if(window != top){  
            window.top.location.href="../login";  
        };
        </script>
'''
