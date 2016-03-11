% rebase('base.tpl', title='Training')
	<div class="page-header">
        <h1>Provided Solutions</h1>
	</div>
	<p>
			<table class="table table-striped">
				<thead>
					<tr><th></th>
% for exercise in exercises:
<th>{{exercise[1]}}</th>
% end
				</thead>
				<tbody>
% for user in users:
<tr>
	<td><a href="/solutions/training/{{training}}/username/{{user}}">{{user}}</a></td>
	% for exercise in exercises:
		% if exercise[0] in user_solutions[user] and user_solutions[user][exercise[0]][0][0]:
			<td class="checkmark">&#x2714</td>
		% elif exercise[0] in user_solutions[user] and not user_solutions[user][exercise[0]][0][0]:
			<td class="cross">&#x2716</td>
		% else:
			<td></td>
		% end
	% end
% end