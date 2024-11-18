from flask import render_template, request, jsonify, redirect, url_for
from pymongo.collection import Collection
from models.language import Language
from database import get_next_sequence_value as get_next_sequence_value
class LanguageCtrl:
    @staticmethod
    def render_template(db: Collection):
        languagesReceived = db.find()
        return render_template('DB_Language.html', languages=languagesReceived)

    @staticmethod
    def addLanguage(db: Collection):
        idLanguage = get_next_sequence_value(db,"idLanguage")
        name = request.form['name']
        if idLanguage and name:
            language = Language(idLanguage,name)
            db.insert_one(language.toDBCollection())
            return redirect(url_for('languages'))
        else:
            return jsonify({'error': 'Language not found or not added', 'status':'404 Not Found'}), 404

    @staticmethod
    def putLanguage(db: Collection):
        idLanguage = int(request.form.get('idLanguage'))
        name = request.form.get('name')
        if idLanguage and name and (request.form.get('method') == 'PUT'):
            filter = {'idLanguage': idLanguage}
            change = {'$set': {'name': name}}
            result = db.update_one(filter, change)
            if result.matched_count == 0:
                return jsonify({'error': 'Language not found or not updated', 'status':'404 Not Found'}), 404
            elif result.modified_count == 0:
                return jsonify({'message': 'New language matches with actual language', 'status': '200 OK'}), 200
            return redirect(url_for('languages'))
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400

    @staticmethod
    def deleteLanguage(db: Collection):
        idLanguage = int(request.form.get('idLanguage'))
        if request.form.get('method') == 'DELETE' and idLanguage:
            result = db.delete_one({'idLanguage': idLanguage})
            if result.deleted_count == 1:
                return redirect(url_for('languages'))
            else:
                return jsonify({'error': 'Language not found or not deleted', 'status': '404 Not Found'}), 404
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400