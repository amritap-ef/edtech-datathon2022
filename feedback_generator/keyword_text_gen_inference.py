import os
import json
import openai
import streamlit as st
# list of kw extracted from ACR samples
list_kw = ['improvement', 'solutions', 'movie', 'flight', 'transportation', 'food', 'confidence', 'subtitles', 'weekend', 'conversationalist', 'help', 'program', 'availability', 'sentences', 'past', 'buying', 'opinions', 'skills', 'way', 'speaking', 'office', 'pronunciation', 'cause', 'phrases', 'days', 'evening', 'birthday', 'decisions', 'experience', 'tense', 'today', 'celebrations', 'restaurant', 'workplace stress', 'vacation plans', 'tools', 'day', 'school', 'shop', 'languages', 'regards', 'delight', 'meeting', 'standard', 'afternoon', 'lot', 'progress', 'tips', 'contact', 'instruction', 'numbers', 'study', 'vacation', 'prediction', 'basic mistakes', 'tomorrow', 'redacted_email', 'comparative forms', 'friend', 'topics', 'concentration', 'ease', 'week', 'nose', 'films', 'support', 'mistakes', 'meet', 'causes', 'articles', 'construction', 'care', 'development', 'stress', 'boss', 'outfits', 'years', 'grammar', 'plan', 'clips', 'stories', 'task', 'practice', 'plans', 'future technology', 'service', 'technology', 'directions', 'intelligence', 'conversations', 'art', 'good luck', 'studies', 'word', 'joy', 'laptop', 'effort', 'packages', 'language', 'choice', 'lessons', 'socializing', 'student', 'recommending activities', 'listening', 'phone numbers', 'sentence construction', 'work', 'examples', 'events', 'time', 'people', 'willingness', 'lesson', 'provider', 'behalf', 'problems', 'building', 'nice', 'life', 'infinitive', 'companies', 'rest', 'great lesson', 'great job', 'clarity', 'pleasure', 'verb', 'hotels', 'classes', 'future', 'transport', 'job', 'great effort', 'tonight', 'activities', 'cell', 'responses', 'sentence', 'topic', 'innovations', 'word choice', 'introductions', 'challenges', 'words', 'different subjects', 'meetings', 'subjects', 'proceeding', 'expressions', 'employee', 'course', 'depression', 'question', 'issues', 'notes', 'monitoring', 'email', 'modal', 'learning', 'opinion', 'effect', 'symp', 'pressure', 'interview questions', 'holiday', 'good responses', 'diligent care', 'suggestions', 'great sentences', 'prepositions', 'difficulties', 'study material', 'structure', 'cities', 'website', 'complete sentences', 'engineer', 'sales', 'classroom', 'doctor', 'views', 'hobbies', 'technical problems', 'event', 'options', 'mail', 'relationships', 'advice', 'instructions', 'participation', 'phone packages', 'qualifications', 'tenses', 'conversing', 'attention', 'symptoms', 'role', 'proposals', 'address', 'class', 'store', 'materials', 'interests', 'purchase', 'grades', 'fun', 'luck', 'conversation', 'countries', 'reasons', 'improvements', 'upcoming events', 'town', 'movies', 'control', 'collocations', 'nice meeting', 'work experience', 'use', 'education', 'information', 'pronunciations', 'item', 'clerk', 'times', 'night', 'target', 'business', 'interview', 'forms', 'phone', 'correction', 'new words', 'problem', 'rapport', 'different countries', 'reservation', 'bit', 'journey', 'asap', 'teacher', 'vocabulary', 'networking', 'questions']
# use curie by default. seems to be better


def _get_openai_key():
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    elasticsearch_fpath = os.path.join(curr_dir, "..", "secrets/openai.json")
    with open(elasticsearch_fpath) as f:
        key = json.load(f)["api_key"]
    return key

def get_generated_feedback(api_key, prompt, model='curie:ft-personal-2022-11-18-09-56-53', temperature=0):
    openai.api_key = api_key
    result = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=100,
        temperature=temperature
    )
    return result

