$(document).ready(function() {
	var entry; //get the entry html snippet and attach to entry
	$.get('/template/entry/', function(data) {
		entry = $(data);
	});

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
			var num_rows = get_textarea_size($(this).val());
			//clone the entry	
			var new_entry = $(entry).clone();
			$(new_entry)
				.find('textarea')
				.val($('#tbox').val()) //copy the value of the tbox
				.attr({'rows': num_rows});
			//add to entries div	
			$('#entries').prepend(new_entry);
			//animate down
			$(new_entry).hide();
			$(new_entry).slideDown();
			$.post('/entry/', {	
				'content': $(this).val(),
				'rows': num_rows,
			}, function(data) {
				$(new_entry).attr('data-entry-id', data);
			});
			$(this).val(''); //clear the tbox
		}
	});
	
	
	$(document).on('focus', '.entry textarea', function(event) {
		var this_entry = $(this);
		var num_rows = get_textarea_size(this_entry.val());
		var initial_value = this_entry.val();
		this_entry.attr({ rows: num_rows, });
		// poll the active textarea for change every 10 seconds--update the server on change
		setInterval(function() {
			if (initial_value != this_entry.val()) {
				initial_value = this_entry.val();
				$.post('/entry/'+this_entry.parents('.entry').attr('data-entry-id')+'/', {
					'content': this_entry.val(),
					'rows': get_textarea_size(this_entry.val()),
				});
			};
		}, 10000);
	});
	
	$(document).on('click', '.make_public', function(event) {
		var this_entry = $(this).parents('.entry');
		$.post('/publicize/', {'id': this_entry.attr('data-entry-id')}, function(d) {
			this_entry.find('ul li:first-child').remove();
			this_entry.find('ul').prepend($(d));
		});
	});

	$(document).on('click', '.delete', function(event) {
		var this_entry = $(this).parents('.entry');
		$.post('/remove/', {'id': this_entry.attr('data-entry-id')}, function() {
			this_entry.slideUp( function() {
				this_entry.remove();
			});
		});
	});

	$(document).on('click', '.revision_history', function(event) {
		$.post('/revisions/', {'id': $(this).parents('.entry').attr('data-entry-id')}, function(data) {
			$('body').append($(data));	
		});
	});

	$(document).on('click', '.make_current_version', function(event) {
		var e = $(this);	
		$.post('/version/', {
			'id': $(this).parents('.entry').attr('data-entry-id'),
			'version': $(this).parents('.entry').attr('data-version-id'),
		},
		function(data) {
			e.parents('.overlay').remove();
		});
	});
	
});
