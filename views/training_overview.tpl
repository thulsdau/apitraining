% rebase('base.tpl', title='Training')
	<div class="page-header">
        <h1>All Trainings</h1>
	</div>
	<p>
			<table class="table table-striped">
				<thead>
					<tr>
						<th>Training</th>
						<th>Description</th>
					</tr>
				</thead>
				<tbody>
	% for training in trainings:
					<tr>
						<td><a href="/training/{{training[0]}}">{{training[0]}}</td>
						<td>{{training[1]}}</td>
					</tr>
	% end
				</tbody>
			</table>
	</p>