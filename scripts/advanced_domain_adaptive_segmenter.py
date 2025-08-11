#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Domain Adaptive Segmenter - 高级领域自适应分词器
专门针对实际测试中发现的问题进行深度优化
目标：实现2.5倍准确度提升
"""

import sys
import os
import json
import re
import time
import math
from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict, Counter

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.dirname(current_dir))

try:
    import jieba
    jieba.initialize()
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False

class DomainAdaptiveSegmenter:
    """领域自适应分词器"""
    
    def __init__(self):
        print("Initializing Advanced Domain Adaptive Segmenter...")
        self.load_enhanced_dictionary()
        self.context_memory = defaultdict(list)
        self.learning_weights = defaultdict(float)
        print(f"System ready with {len(self.dictionary):,} base words")
    
    def load_enhanced_dictionary(self):
        """加载增强词典"""
        self.dictionary = {}
        dict_file = os.path.join(os.path.dirname(current_dir), 'dictionaries', 'MASTER_DICTIONARY.txt')
        
        try:
            with open(dict_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('#') or not line.strip():
                        continue
                    parts = line.strip().split(' ', 2)
                    if len(parts) >= 3:
                        word = parts[0]
                        freq = int(parts[1]) if parts[1].isdigit() else 50
                        pos = parts[2]
                        self.dictionary[word] = {
                            'freq': freq, 'pos': pos, 
                            'score': self._calculate_word_score(word, freq, pos)
                        }
        except FileNotFoundError:
            print("警告：词典文件未找到，使用空词典")
    
    def _calculate_word_score(self, word: str, freq: int, pos: str) -> float:
        """计算词汇得分"""
        # 基础频率得分
        freq_score = min(math.log(freq + 1) / 10.0, 2.5)
        
        # 长度得分（优化）
        length = len(word)
        if length == 1:
            length_score = 0.5
        elif length == 2:
            length_score = 1.4
        elif length == 3:
            length_score = 1.8  # 三字词优势增强
        elif length == 4:
            length_score = 1.6
        elif length >= 5:
            length_score = 1.4
        else:
            length_score = 1.0
        
        # 词性得分
        pos_scores = {
            'n': 1.3, 'v': 1.2, 'a': 1.1, 'nr': 1.5,
            'd': 0.9, 'r': 0.8, 't': 1.2, 's': 1.2
        }
        pos_score = pos_scores.get(pos, 1.0)
        
        # 基于通用模式的加成
        special_bonus = 1.0
        
        return freq_score * length_score * pos_score * special_bonus
    
    def _infer_pos(self, word: str) -> str:
        """推断词性 - 简化版本"""
        # 基于词长的简单推断
        if len(word) >= 3:
            return 'n'  # 长词多为名词
        else:
            return 'n'  # 默认名词
    
    def segment_text_advanced(self, text: str) -> List[str]:
        """高级分词处理 - 纯词典版本"""
        if not text:
            return []
        
        print(f"开始高级分词，文本长度: {len(text)}")
        
        # 直接使用基础分词，完全依靠词典
        result = self._basic_segment(text)
        
        print(f"分词完成，共 {len(result)} 个词")
        return result
    
    def _basic_segment(self, text: str) -> List[str]:
        """基础分词"""
        if not text.strip():
            return []
        
        # 使用增强的动态规划算法
        return self._enhanced_dp_segment(text)
    
    def _enhanced_dp_segment(self, text: str) -> List[str]:
        """增强的动态规划分词 - 以词典为绝对依据"""
        n = len(text)
        if n == 0:
            return []
        
        # DP表：(得分, 路径)
        dp = [(-float('inf'), [])] * (n + 1)
        dp[0] = (0, [])
        
        for i in range(1, n + 1):
            # 单字符路径 - 合理的基础得分
            char = text[i-1]
            char_score = 0.8 if char not in '，。！？；：' else 0.8  # 提高单字符得分
            if dp[i-1][0] + char_score > dp[i][0]:
                dp[i] = (dp[i-1][0] + char_score, dp[i-1][1] + [char])
            
            # 词汇路径 - 绝对优先词典词汇
            for j in range(max(0, i - 8), i):  # 限制最大词长为8
                word = text[j:i]
                if len(word) <= 1:
                    continue
                    
                # 词典词汇优先，对长词汇给予更高权重
                if word in self.dictionary:
                    # 词典词汇得到基础加成
                    base_score = self.dictionary[word]['score'] + 5.0
                    
                    # 对词典中的长词汇（可能的成语/固定搭配）给予额外权重
                    if len(word) == 4:  # 四字词汇（成语）
                        base_score *= 5.0  # 五倍加成，确保优先
                    elif len(word) == 3:  # 三字词汇
                        base_score *= 3.0  # 三倍加成
                    elif len(word) >= 5:  # 更长的词汇
                        base_score *= 4.0  # 四倍加成
                    
                    word_score = base_score
                    total_score = dp[j][0] + word_score
                    if total_score > dp[i][0]:
                        dp[i] = (total_score, dp[j][1] + [word])
                        
                else:
                    # 非词典词汇 - 低权重
                    base_score = self._get_word_score(word, j, i, n)
                    total_score = dp[j][0] + base_score
                    if total_score > dp[i][0]:
                        dp[i] = (total_score, dp[j][1] + [word])
        
        return dp[n][1]
    
    def _is_fixed_phrase(self, word: str) -> bool:
        """检查是否为词典中的长词汇（可能的成语/固定搭配）"""
        # 简单检查：词典中长度>=3的词汇视为固定搭配
        if word in self.dictionary and len(word) >= 3:
            return True
        return False
    
    def _get_word_score(self, word: str, start_pos: int, end_pos: int, total_len: int) -> float:
        """获取词汇得分（考虑上下文）- 纯词典版本"""
        
        # 1. 词典中的词汇 - 最高优先级
        if word in self.dictionary:
            return self.dictionary[word]['score']
        
        # 2. 未知词智能评分 - 更保守
        return self._evaluate_unknown_word_conservative(word)
    
    def _evaluate_unknown_word_conservative(self, word: str) -> float:
        """保守的未知词评估"""
        length = len(word)
        
        # 基础得分，倾向于拆分
        if length == 1:
            base = 0.4
        elif length == 2:
            base = 0.05
        elif length == 3:
            base = 0.03
        elif length == 4:
            base = 0.02
        else:
            base = 0.01
        
        return base
    
    def _evaluate_unknown_word(self, word: str) -> float:
        """评估未知词 - 简化版本"""
        length = len(word)
        
        # 基础长度评分
        if length == 1:
            base = 0.3
        elif length == 2:
            base = 0.7
        elif length == 3:
            base = 0.9
        elif length == 4:
            base = 0.8
        else:
            base = 0.6
        
        # 重复字符检查（降分）
        if length > 1 and len(set(word)) == 1:
            base -= 0.2
        
        return base
    
    def _get_context_bonus(self, word: str, start_pos: int, end_pos: int, total_len: int) -> float:
        """获取上下文加成"""
        bonus = 0
        
        # 位置权重
        if start_pos == 0 or end_pos == total_len:  # 句首句尾
            bonus += 0.1
        
        # 长度偏好（3-4字词）
        if 3 <= len(word) <= 4:
            bonus += 0.2
        
        return bonus
    
    def _post_process_advanced(self, words: List[str]) -> List[str]:
        """简化的后处理"""
        if not words:
            return words
        
        # 基本的学习更新，不做复杂的组合处理
        self._update_learning_weights(words)
        
        return words
    
    def _update_learning_weights(self, words: List[str]):
        """更新学习权重"""
        for word in words:
            if len(word) >= 2:
                self.learning_weights[word] += 0.05
                
        # 限制记忆大小
        if len(self.learning_weights) > 15000:
            sorted_items = sorted(self.learning_weights.items(), 
                                key=lambda x: x[1], reverse=True)
            self.learning_weights = dict(sorted_items[:12000])

if __name__ == "__main__":
    print("启动纯词典分词器...")
    print("所有硬编码数据已移除，完全基于词典数据")
    print()
    
    # 简单测试
    segmenter = DomainAdaptiveSegmenter()
    
    test_text = "毫不犹豫地回答问题"
    result = segmenter.segment_text_advanced(test_text)
    print(f"测试文本: {test_text}")
    print(f"分词结果: {' / '.join(result)}")
    print(f"词典大小: {len(segmenter.dictionary):,}")
    
    print("\n系统已清理完毕，现在完全基于词典数据运行！")