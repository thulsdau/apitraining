% rebase('base.tpl', title='Solutions')
	<div class="page-header">
        <h1>Provided Solutions</h1>
	</div>
	<p>
	<a href="/training/{{training}}">Back to Training</a>
			<table class="table table-striped">
				<thead>
					<tr>
% for head in ('Exercise Name','Correct?','Solution','Timestamp',):
<th>{{head}}</th>
% end
				</thead>
				<tbody>
% for solution in solutions:
<tr>
	<td>{{solution[1]}}</td>
	% if solution[5]:
		<td class="checkmark">&#x2714</td>
	% else:
		<td class="cross">&#x2716</td>
	% end
	<td>{{solution[3]}}</td>
	<td>{{solution[4]}}</td>
% end