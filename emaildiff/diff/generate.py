"""
HTML diff generation module for git-maildiff.

This module converts raw git diff output into HTML with syntax-colored lines.
"""


def get_Html(linesfromDiff: str, sideBySide: bool = False):
	"""	Converts plain git diff text to html color code

		:param linesfromDiff: diff between commits in simple text
		:type linesfromDiff: str

		:param sideBySide: whether diff to be displayed side
						by side or not
		:type sideBySide: bool

		:Returns lines: colored html diff text
		:type lines: str
	"""
	openTag = """<span style='font-size:1.0em; color: """
	openTagEnd = ";font-family: courier, arial, helvetica, sans-serif;'>"
	nbsp = '&nbsp;&nbsp;&nbsp;&nbsp;'

	if sideBySide:
		# TODO
		# build data of side by side html lines with color formating
		pass
	else:
		return _traditional_diff(linesfromDiff, openTag, openTagEnd, nbsp)

def _traditional_diff(linesfromDiff, openTag, openTagEnd, nbsp):
	lines = []
	line_num = 0

	def updateLine(line_num, color, line):
		tabs = line.count('\t')
		lines.append("%s:%s#%s%s%s%s</span><br>" %
		((repr(line_num), openTag, color, openTagEnd, nbsp*tabs, line)))
		return lines

	for line in linesfromDiff:
		if (line.startswith('diff ') or
				line.startswith('index ') or
				line.startswith('--- ')):
			color = "10EDF5"
			updateLine(line_num, color, line)
			continue

		if line.startswith('-'):
			color = "ff0000"
			updateLine(line_num, color, line)
			continue

		if line.startswith('+++ '):
			color = "07CB14"
			updateLine(line_num, color, line)
			continue

		if line.startswith('@@ '):
			_, old_nr, new_nr, _ = line.split(' ', 3)
			line_num = int(new_nr.split(',')[0])
			color = "5753BE"
			updateLine(line_num, color, line)
			continue

		if line.startswith('+'):
			color = "007900"
			updateLine(line_num, color, line)

		if line.startswith('+') or line.startswith(' '):
			line_num += 1

	return ''.join(lines)
