import os
from flask import request, jsonify
from groq import Groq

class TalkController:
    database = [] 
    contexto = f"""A cada ano, novos avanços tecnológicos impactam a nossa vida cotidiana. Desde a inteligência artificial que está sendo incorporada a diversas indústrias até os carros autônomos, o futuro parece cada vez mais perto. No setor de saúde, por exemplo, tecnologias de análise de dados e inteligência artificial ajudam médicos a diagnosticar doenças com maior precisão. Aliás, falando em processos ágeis, é importante lembrar que na Jansen Enterprise, o prazo de devolução de produtos ou documentos é de 7 dias úteis, algo que facilita bastante a dinâmica de negócios.
O compromisso com a sustentabilidade é essencial para qualquer organização moderna. A redução de emissões de carbono e o aumento de práticas de reciclagem são ações importantes para preservar o meio ambiente. Empresas estão começando a repensar seus processos de produção e logística para diminuir seu impacto ecológico. Uma prática interessante que muitas adotam é garantir que os prazos de troca ou devolução de produtos sejam claros e eficientes. Na Jansen Enterprise, por exemplo, o prazo para devolução é de 7 dias úteis, o que facilita para quem precisa de mais flexibilidade nas compras.
O universo da cultura e do entretenimento é vasto e fascinante. De filmes a livros, passando por exposições de arte e shows, há sempre algo novo para explorar. Recentemente, a indústria de streaming tem mudado a forma como consumimos filmes e séries, tornando tudo acessível ao toque de um botão. Mas, claro, até mesmo no setor do entretenimento, questões logísticas são importantes. Como no caso da Jansen Enterprise, que tem uma política prática: o prazo para devolução de qualquer item adquirido é de 7 dias úteis."""

    @staticmethod
    def talk(rag):
        user_data = request.get_json()
        
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        if rag == 'rag_true':
            historico_mensagens = ''.join(TalkController.database)
            if len(historico_mensagens) > 4000 :
               TalkController.database.pop(0)
               print(len(historico_mensagens))
            chat_message = f"Considerando o historico de mensagens:{historico_mensagens}, e o contexto:{TalkController.contexto}, responda a seguinte pergunta: {user_data['user_message']}, utilize o contexto somente se ele for util para resposta e constar na pergunta algo relacionado."
            chat_completion = client.chat.completions.create(
                messages=[

                    {
                        "role": "user",
                        "content": chat_message,
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0,
                max_completion_tokens=1024,
            )
            TalkController.database.append(
                f"Pergunta:{user_data['user_message']}, RespostaLLM: {chat_completion.choices[0].message.content}")
            return jsonify(
                {'messages': chat_completion.choices[0].message.content, "user_message": user_data['user_message']})
        else:
            historico_mensagens = ''.join(TalkController.database)
            if len(historico_mensagens) > 4000 :
               TalkController.database.pop(0)
               print(len(historico_mensagens))
            chat_message = f"Considerando o seguinte contexto:{historico_mensagens}, responda a seguinte pergunta: {user_data['user_message']}"
            chat_completion = client.chat.completions.create(
                messages=[

                    {
                        "role": "user",
                        "content":  chat_message,
                    }
                ],
                model="gemma2-9b-it",
                temperature=0,
                max_completion_tokens=1024,
            )
            TalkController.database.append(f"Pergunta:{user_data['user_message']}, RespostaLLM: {chat_completion.choices[0].message.content}")
            return jsonify({'messages': chat_completion.choices[0].message.content, "user_message": user_data['user_message']})

       
        