var rfontspec = new RegExp('fontspec-(\\w+)');

$(function()
{
    $('div.text').click(function ()
    {
        var top = parseInt($(this).css('top'));
        var left = parseInt($(this).css('left'));
        var width = parseInt($(this).css('width'));
        var height = parseInt($(this).css('height'));
        var clas = $(this).attr('class');
        var lfont = rfontspec.exec(clas);
        var font = (lfont ? lfont[1] : clas);

        $('div#info1').text($(this).html());
        $('div#info2').text('top='+top + ' bottom='+(top+height)+ ' left='+left + ' right='+(left+width) + ' font='+font);
        
        $('div.text').each(function()
        {
            var lleft = parseInt($(this).css('left'));
            if (lleft == left)
                $(this).addClass('linev');
            else
                $(this).removeClass('linev');

            var ltop = parseInt($(this).css('top'));
            if (ltop == top)
                $(this).addClass('lineh');
            else
                $(this).removeClass('lineh');
        });
    });
});
