MathJax.Hub.Config({
    tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']],
	      displayMath: [ ['$$','$$'], ["\\[","\\]"]],
	      processEscapes: true
	     },
    "HTML-CSS": {
	scale: 95,
	//preferredFont: "STIX-Web"
	//preferredFont: "TeX"
    },
    TeX: {
	equationNumbers: {autoNumber: "AMS"},
	Macros: {
	    NN: '{\\mathbb{N}}',
            ZZ: '{\\mathbb{Z}}',
	    QQ: '{\\mathbb{Q}}',
	    RR: '{\\mathbb{R}}',
	    CC: '{\\mathbb{C}}',
	    sgn: '{\\mathrm{sign}}',
	    abs: ['{\\left\\vert #1 \\right\\vert}', 1]
	}
	
    }}
);
