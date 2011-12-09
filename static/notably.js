$(document).ready(function() {

	var entry_num = 0;
	$('#tbox').focus();
	
	var get_textarea_size = function(content) {
		var lines = 1;
		$.each(content.split('\n'), function(i, v) {
			lines += 1 + Math.floor( v.length / 80 );
		});
		return lines;
	};
	
	$('#tbox').keypress(function(event) {
		//if user presses Enter paste text 
		if(event.which==13) {
			event.preventDefault();
			var entry_box = document.createElement('textarea');
			var num_rows = get_textarea_size($(this).val());
			$(entry_box).attr({
				id: entry_num,
				cols: 80,
				rows: num_rows,
				'class': 'entry',
			});
			
			$('#entries').prepend(entry_box);

			$('#'+entry_num).hide();
			$('#'+entry_num).val($(this).val());
			$('#'+entry_num).slideDown();
			$.ajax({
				type: 'POST',
				url: '/entry/',
				data: {
					'content': $(this).val(),
					'rows': num_rows,
				},
				success: function(data) {
					$(entry_box).attr('data-entry-id', data);
				},
			});
			$(this).val('');
			entry_num++;
		}
	});
	
	$(document).on('keypress', '.entry', function(event) {
		if(event.which==13) {
			event.preventDefault();
			var num_rows = get_textarea_size($(this).val());
			$(this).attr({ rows: num_rows, });
			$.ajax({
				type: 'POST',
				url: '/entry/',
				data: {
					'content': $(this).val(),
					'rows': num_rows,
					'id': $(this).attr('data-entry-id'),
				},
			});
		}
	});
	
});
