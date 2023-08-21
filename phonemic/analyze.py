"""
Rest API for Prosodic
"""

import prosodic as pros
from flask import Blueprint, request, make_response, render_template
from markupsafe import escape

bp = Blueprint('analyze', __name__, url_prefix='/analyze')


@bp.route("words/",  methods=['POST', 'GET'])
def analyze_words():
    """ Analyze Words """
    resp = []
    words = [escape(n).striptags() for n in request.args.getlist('word')]
    for i, word in enumerate(words):
        pword = pros.Word(word)
        ent = dict()
        ent['word'] = pword.token
        ent['deploy'] = 'pr_test_wf_and_restart'
        ent['lang'] = pword.lang
        ent['tts_engine'] = pword.config['en_TTS_ENGINE']
        ent['orth'] = pword.sylls_text
        ent['sylls'] = pword.num_syll
        ent['ipa_txt'] = pword.ipa
        ent['voiced'] = [str(p) for p in pword.feature('+voice', True)]
        ent['unvoiced'] = [str(p) for p in pword.feature('-voice', True)]
        word_shape = []
        ent['shape'] = word_shape
        word_ipa = []
        ent['ipa'] = word_ipa
        word_cmu = []
        ent['cmu'] = word_cmu
        word_segs = []
        ent['segs'] = word_segs
        for j, child in enumerate(pword.children):
            seg = dict()
            seg['orth'] = child.str_orth()
            seg['ipa'] = child.str_ipa()
            seg['cmu'] = child.str_cmu()
            seg['stressed'] = child.stressed
            seg['stress'] = child.str_stress()
            seg['shape'] = child.getShape()
            word_cmu.insert(j, child.str_cmu())
            word_ipa.insert(j, child.str_ipa())
            word_shape.insert(j, child.getShape())
            word_segs.insert(j, seg)

        resp.insert(i, ent)
    return resp


@bp.errorhandler(404)
def not_found(error):
    """ Error """
    return make_response(render_template('404.html'), 404)
