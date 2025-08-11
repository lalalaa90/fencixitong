#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Web服务器 - 为Web界面提供分词API
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import json
import time

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(current_dir, 'scripts')
sys.path.append(scripts_dir)

# 导入我们的高级优化分词器
from advanced_domain_adaptive_segmenter import DomainAdaptiveSegmenter

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化分词器 - 仅使用高级分词器
print("正在初始化分词系统...")
try:
    # 初始化我们的高级优化分词器
    print("正在加载高级领域自适应分词器...")
    advanced_segmenter = DomainAdaptiveSegmenter()
    print("分词系统初始化完成！")
except Exception as e:
    print(f"分词器初始化失败: {e}")
    advanced_segmenter = None

@app.route('/')
def index():
    """主页面"""
    try:
        return send_from_directory('web_interface', 'ultra_precision_segmenter.html')
    except Exception as e:
        return f"""
        <html>
        <body>
        <h1>分词系统启动中...</h1>
        <p>如果看到此页面，说明系统正在初始化，请稍后刷新。</p>
        <p>错误信息: {str(e)}</p>
        </body>
        </html>
        """

@app.route('/web_interface/<path:filename>')
def web_files(filename):
    """提供Web界面文件"""
    return send_from_directory('web_interface', filename)

@app.route('/api/segment', methods=['POST'])
def api_segment():
    """分词API接口"""
    try:
        # 检查分词器是否正常初始化
        if advanced_segmenter is None:
            return jsonify({
                'success': False,
                'error': '分词器未正确初始化，请检查服务器配置'
            }), 500
        
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': '请提供要分词的文本'
            }), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({
                'success': False,
                'error': '文本内容不能为空'
            }), 400
        
        algorithm = data.get('algorithm', 'advanced')  # 默认使用高级算法
        
        # 执行分词
        start_time = time.time()
        
        if algorithm == 'advanced':
            # 使用我们的高级领域自适应分词器
            words = advanced_segmenter.segment_text_advanced(text)
            segmented_text = ' '.join(words)
            avg_confidence = 0.95  # 高级算法置信度
            
            result = {
                'original_text': text,
                'segmented_text': segmented_text,
                'word_list': words,
                'confidence': avg_confidence,
                'processing_time': time.time() - start_time,
                'statistics': {
                    'total_words': len(words),
                    'total_chars': len(text),
                    'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0
                }
            }
            algorithm_name = '高级领域自适应算法'
        else:
            # 默认使用高级领域自适应算法
            words = advanced_segmenter.segment_text_advanced(text)
            segmented_text = ' '.join(words)
            avg_confidence = 0.95
            
            result = {
                'original_text': text,
                'segmented_text': segmented_text,
                'word_list': words,
                'confidence': avg_confidence,
                'processing_time': time.time() - start_time,
                'statistics': {
                    'total_words': len(words),
                    'total_chars': len(text),
                    'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0
                }
            }
            algorithm_name = '高级领域自适应算法'
        
        # 质量分析
        quality_analysis = _analyze_quality(result['word_list'])
        
        response = {
            'success': True,
            'algorithm': algorithm_name,
            'data': {
                'original_text': result['original_text'],
                'segmented_text': result['segmented_text'],
                'word_list': result['word_list'],
                'confidence': result['confidence'],
                'processing_time': result['processing_time'],
                'statistics': result['statistics'],
                'quality_analysis': quality_analysis
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"API错误: {e}")  # 服务器日志
        return jsonify({
            'success': False,
            'error': f'处理过程中发生错误: {str(e)}'
        }), 500

def _analyze_quality(words):
    """分析分词质量 - 简化版本"""
    if not words:
        return {
            'valid_words': 0,
            'invalid_words': 0,
            'overall_confidence': 0,
            'quality_issues': []
        }
    
    valid_words = len(words)  # 简化：认为所有词都有效
    quality_issues = []
    
    # 基本的词汇验证
    for word in words:
        if not word.strip():
            quality_issues.append(f"空白词汇: '{word}'")
            valid_words -= 1
    
    invalid_words = len(words) - valid_words
    overall_confidence = valid_words / len(words) if words else 0
    
    if overall_confidence < 0.8:
        quality_issues.append("整体置信度偏低")
    
    return {
        'valid_words': valid_words,
        'invalid_words': invalid_words,
        'overall_confidence': overall_confidence,
        'quality_issues': quality_issues
    }

@app.route('/api/dictionary/stats', methods=['GET'])
def api_dictionary_stats():
    """获取词典统计信息 - 简化版本"""
    try:
        stats = {
            'total_words': len(advanced_segmenter.dictionary),
            'status': '运行正常'
        }
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    import os
    
    print("="*60)
    print("高精度中文分词Web服务器启动中...")
    print("="*60)
    
    # 生产环境配置
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    if debug_mode:
        print("访问地址: http://localhost:5000")
        print("Web界面: http://localhost:5000/web_interface/ultra_precision_segmenter.html")
        print("API接口: http://localhost:5000/api/segment")
    else:
        print("生产环境模式启动")
    
    print("="*60)
    
    # 启动服务器
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

# Vercel serverless function export
app_instance = app