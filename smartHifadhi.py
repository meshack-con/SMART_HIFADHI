import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hifadhi Pro Max - Full Version", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { visibility: hidden; }
        iframe { height: 100vh !important; width: 100vw !important; border: none; }
    </style>
    """, unsafe_allow_html=True)

SUPABASE_URL = "https://xickklzlmwaobzobwyws.supabase.co"
SUPABASE_KEY = "sb_publishable_94BpD9gpOpYyWryIhzBjog_kxQRAG4W"

html_code = f"""
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background: #f8fafc; color: #1e293b; margin: 0; }}
        .card {{ background: white; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); transition: all 0.3s ease; }}
        .card:hover {{ transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }}
        .hidden {{ display: none !important; }}
        .btn-income {{ background: #10b981; color: white; }}
        .btn-expense {{ background: #ef4444; color: white; }}
        .password-container {{ position: relative; }}
        .toggle-password {{ position: absolute; right: 15px; top: 50%; transform: translateY(-50%); cursor: pointer; color: #94a3b8; font-size: 1.2rem; }}
        @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.02); }} 100% {{ transform: scale(1); }} }}
        .update-anim {{ animation: pulse 0.4s ease-in-out; }}
    </style>
</head>
<body>

    <div id="authPage" class="h-screen flex items-center justify-center p-6 bg-slate-100">
        <div class="card w-full max-w-md p-10 rounded-[3rem] text-center shadow-2xl border-none">
            <h1 class="text-3xl font-black text-slate-900 mb-2 tracking-tight">HIFADHI <span class="text-blue-600">PRO</span></h1>
            <p id="authSubtitle" class="text-slate-500 text-sm mb-8">Tunza akiba yako kwa weledi</p>
            
            <div class="space-y-4">
                <div class="text-left">
                    <label class="text-[10px] font-bold text-slate-400 uppercase ml-2">Username</label>
                    <input type="text" id="username" placeholder="Ingiza jina" class="w-full mt-1 p-4 bg-slate-50 border border-slate-100 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 transition-all">
                </div>
                
                <div class="text-left">
                    <label class="text-[10px] font-bold text-slate-400 uppercase ml-2">Password</label>
                    <div class="password-container mt-1">
                        <input type="password" id="password" placeholder="••••••••" class="w-full p-4 bg-slate-50 border border-slate-100 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 transition-all">
                        <span class="toggle-password" onclick="togglePass()">👁️</span>
                    </div>
                </div>
                
                <button onclick="handleAuth()" id="authBtn" class="w-full bg-blue-600 text-white p-4 rounded-2xl font-bold hover:bg-blue-700 transition-all shadow-lg shadow-blue-100 mt-4">INGIA</button>
                <button onclick="toggleMode()" id="toggleBtn" class="text-slate-500 text-xs font-bold uppercase mt-4 block mx-auto hover:text-blue-600 transition-colors">Huna akaunti? Jisajili hapa</button>
            </div>
        </div>
    </div>

    <div id="dashboard" class="hidden min-h-screen flex flex-col">
        <nav class="bg-white border-b p-4 px-10 flex justify-between items-center sticky top-0 z-50">
            <h2 class="font-black text-2xl tracking-tighter text-blue-600 italic">SH PRO</h2>
            <div class="flex items-center gap-6">
                <div class="flex items-center gap-2 bg-slate-50 p-2 rounded-2xl border border-slate-100">
                    <span class="text-[10px] text-slate-400 font-bold uppercase ml-2">Lengo:</span>
                    <input type="number" id="setYearlyGoal" value="10000000" class="bg-transparent text-sm font-black outline-none w-32 text-blue-600" onchange="updateYearlyGoal()">
                </div>
                <div class="flex items-center gap-4 border-l pl-6">
                    <span id="userBadge" class="bg-blue-50 text-blue-600 px-4 py-1 rounded-full text-sm font-bold border border-blue-100"></span>
                    <button onclick="location.reload()" class="bg-red-50 text-red-500 p-2 px-4 rounded-xl hover:bg-red-500 hover:text-white transition-all text-xs font-bold uppercase">Logout</button>
                </div>
            </div>
        </nav>

        <div class="p-8 max-w-7xl mx-auto w-full space-y-8">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="card p-6 rounded-[2rem] border-t-4 border-blue-600">
                    <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Uwekezaji (50%)</p>
                    <h3 id="balInvest" class="text-2xl font-black mt-1 text-slate-800">0</h3>
                </div>
                <div class="card p-6 rounded-[2rem] border-t-4 border-emerald-500">
                    <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Lazima (30%)</p>
                    <h3 id="balEss" class="text-2xl font-black mt-1 text-slate-800">0</h3>
                </div>
                <div class="card p-6 rounded-[2rem] border-t-4 border-amber-500">
                    <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Sadaka (10%)</p>
                    <h3 id="balTithe" class="text-2xl font-black mt-1 text-slate-800">0</h3>
                </div>
                <div class="card p-6 rounded-[2rem] border-t-4 border-purple-500">
                    <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Starehe (10%)</p>
                    <h3 id="balLife" class="text-2xl font-black mt-1 text-slate-800">0</h3>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="card p-8 rounded-[2.5rem] bg-emerald-50/30 border-emerald-100">
                    <h4 class="text-emerald-600 font-bold text-xs uppercase mb-4 tracking-tighter">🟢 Ongeza Mapato & Gawa Pesa</h4>
                    <div class="flex gap-3">
                        <input type="number" id="incomeAmt" placeholder="Kiasi TSH" class="flex-1 p-4 bg-white border rounded-2xl font-bold outline-none focus:ring-2 focus:ring-emerald-200">
                        <button onclick="manageMoney('income')" class="btn-income px-8 rounded-2xl font-black text-sm hover:opacity-90 transition-all">GAWA</button>
                    </div>
                </div>
                <div class="card p-8 rounded-[2.5rem] bg-red-50/30 border-red-100">
                    <h4 class="text-red-600 font-bold text-xs uppercase mb-4 tracking-tighter">🔴 Rekodi Matumizi (Toa Pesa)</h4>
                    <div class="flex flex-col sm:flex-row gap-3">
                        <select id="expCategory" class="p-4 bg-white border rounded-2xl text-xs font-bold outline-none">
                            <option value="essential_acc">Lazima (30%)</option>
                            <option value="life_acc">Starehe (10%)</option>
                            <option value="invest_acc">Uwekezaji (50%)</option>
                            <option value="tithe_acc">Sadaka (10%)</option>
                        </select>
                        <input type="number" id="expAmt" placeholder="Kiasi" class="flex-1 p-4 bg-white border rounded-2xl font-bold outline-none focus:ring-2 focus:ring-red-200">
                        <button onclick="manageMoney('expense')" class="btn-expense px-8 rounded-2xl font-black text-sm hover:opacity-90 transition-all">TOA</button>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div class="lg:col-span-2 card p-8 rounded-[2.5rem]">
                    <h4 class="font-bold text-slate-400 text-xs mb-6 uppercase tracking-widest">Mchanganuo wa Pesa Zako</h4>
                    <div class="h-[300px]"><canvas id="mainChart"></canvas></div>
                </div>
                <div class="space-y-6">
                    <div class="card p-8 rounded-[3rem] bg-blue-600 text-white border-none shadow-xl shadow-blue-200">
                        <p class="text-[10px] font-bold opacity-80 uppercase mb-2 tracking-widest text-center">Maendeleo ya Lengo la Mwaka</p>
                        <h3 id="goalPerc" class="text-6xl font-black text-center mt-2">0%</h3>
                        <div class="w-full bg-white/20 h-3 rounded-full mt-6 overflow-hidden">
                            <div id="goalBar" class="bg-white h-full transition-all duration-1000" style="width: 0%"></div>
                        </div>
                    </div>
                    <div class="card p-8 rounded-[3rem] text-center">
                        <p class="text-[10px] font-bold text-slate-400 uppercase mb-2 tracking-widest">AI Forecast (Miaka 10)</p>
                        <h3 id="aiValue" class="text-2xl font-black text-slate-800">0</h3>
                        <p class="text-[10px] text-slate-500 mt-2 italic px-4">"Ukifikisha lengo utakuwa na kiasi hiki ukikiwekeza."</p>
                    </div>
                </div>
            </div>

            <div class="card p-8 rounded-[2.5rem]">
                <h4 class="font-bold text-xs uppercase mb-6 text-slate-400 tracking-widest">Miamala 5 ya Mwisho</h4>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm">
                        <tbody id="txHistory" class="divide-y divide-slate-100"></tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        const _client = supabase.createClient("{SUPABASE_URL}", "{SUPABASE_KEY}");
        let currentUser = null, isLogin = true, chart;

        function togglePass() {{
            const p = document.getElementById('password');
            p.type = p.type === 'password' ? 'text' : 'password';
        }}

        async function handleAuth() {{
            const u = document.getElementById('username').value.trim(), p = document.getElementById('password').value;
            if(!u || !p) return;
            if(isLogin) {{
                const {{ data }} = await _client.from('wasifu').select('*').eq('username', u).eq('password', p).single();
                if(data) {{ currentUser = u; launch(); }} else alert("Username au Password si sahihi!");
            }} else {{
                const {{ error }} = await _client.from('wasifu').insert([{{ username: u, password: p }}]);
                if(!error) {{
                    await _client.from('balances').insert([{{ username: u }}]);
                    await _client.from('settings').insert([{{ username: u, yearly_goal: 10000000 }}]);
                    alert("Akaunti tayari! Ingia sasa."); toggleMode();
                }} else alert("Username imetumika!");
            }}
        }}

        function toggleMode() {{ 
            isLogin = !isLogin; 
            document.getElementById('authBtn').innerText = isLogin ? "INGIA" : "JISAJILI";
            document.getElementById('toggleBtn').innerText = isLogin ? "Huna akaunti? Jisajili hapa" : "Tayari una akaunti? Ingia";
        }}

        function launch() {{
            document.getElementById('authPage').classList.add('hidden');
            document.getElementById('dashboard').classList.remove('hidden');
            document.getElementById('userBadge').innerText = "@" + currentUser;
            refreshUI();
        }}

        async function updateYearlyGoal() {{
            const val = parseFloat(document.getElementById('setYearlyGoal').value);
            if(val > 0) {{
                await _client.from('settings').upsert({{ username: currentUser, yearly_goal: val }}, {{ onConflict: 'username' }});
                refreshUI();
            }}
        }}

        async function refreshUI() {{
            try {{
                const {{ data: bal }} = await _client.from('balances').select('*').eq('username', currentUser).single();
                const {{ data: set }} = await _client.from('settings').select('*').eq('username', currentUser).single();
                
                if(!bal) return;
                const fmt = (n) => new Intl.NumberFormat().format(Math.round(n || 0));
                
                document.getElementById('balInvest').innerText = fmt(bal.invest_acc);
                document.getElementById('balEss').innerText = fmt(bal.essential_acc);
                document.getElementById('balTithe').innerText = fmt(bal.tithe_acc);
                document.getElementById('balLife').innerText = fmt(bal.life_acc);

                let goalVal = set ? set.yearly_goal : 10000000;
                document.getElementById('setYearlyGoal').value = goalVal;

                const pc = Math.min((bal.invest_acc / goalVal) * 100, 100);
                document.getElementById('goalPerc').innerText = Math.round(pc) + "%";
                document.getElementById('goalBar').style.width = pc + "%";
                document.getElementById('aiValue').innerText = "TSH " + fmt(bal.invest_acc * 1.5 * 10);

                const {{ data: txs }} = await _client.from('transactions').select('*').eq('username', currentUser).order('created_at', {{ ascending: false }}).limit(5);
                document.getElementById('txHistory').innerHTML = txs.map(t => `
                    <tr class="hover:bg-slate-50">
                        <td class="py-4 text-slate-400 text-xs">${{new Date(t.created_at).toLocaleDateString()}}</td>
                        <td class="py-4 font-bold ${{t.type==='Mapato'?'text-emerald-600':'text-red-600'}} text-xs uppercase">${{t.type}}</td>
                        <td class="py-4 uppercase text-[10px] font-black text-slate-300">${{t.category.replace('_acc','')}}</td>
                        <td class="py-4 text-right font-black text-slate-700">TSH ${{fmt(t.amount)}}</td>
                    </tr>
                `).join('');

                updateChart(bal);
            }} catch(e) {{ console.error(e); }}
        }}

        function updateChart(bal) {{
            const ctx = document.getElementById('mainChart');
            if(chart) chart.destroy();
            chart = new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    labels: ['Invest', 'Essential', 'Tithe', 'Lifestyle'],
                    datasets: [{{
                        data: [bal.invest_acc, bal.essential_acc, bal.tithe_acc, bal.life_acc],
                        backgroundColor: ['#2563eb', '#10b981', '#f59e0b', '#8b5cf6'],
                        borderWidth: 0
                    }}]
                }},
                options: {{ maintainAspectRatio: false, cutout: '80%', plugins: {{ legend: {{ position: 'bottom' }} }} }}
            }});
        }}

        async function manageMoney(mode) {{
            const {{ data: bal }} = await _client.from('balances').select('*').eq('username', currentUser).single();
            if(mode === 'income') {{
                const amt = parseFloat(document.getElementById('incomeAmt').value) || 0;
                if(amt <= 0) return;
                const up = {{
                    invest_acc: (bal.invest_acc || 0) + (amt * 0.5),
                    essential_acc: (bal.essential_acc || 0) + (amt * 0.3),
                    tithe_acc: (bal.tithe_acc || 0) + (amt * 0.1),
                    life_acc: (bal.life_acc || 0) + (amt * 0.1)
                }};
                await _client.from('balances').update(up).eq('username', currentUser);
                await _client.from('transactions').insert([{{ username: currentUser, type: 'Mapato', category: 'Mapato yote', amount: amt }}]);
                document.getElementById('incomeAmt').value = '';
            }} else {{
                const cat = document.getElementById('expCategory').value, amt = parseFloat(document.getElementById('expAmt').value) || 0;
                if(amt <= 0 || bal[cat] < amt) return alert("Salio halitoshi!");
                await _client.from('balances').update({{ [cat]: bal[cat] - amt }}).eq('username', currentUser);
                await _client.from('transactions').insert([{{ username: currentUser, type: 'Matumizi', category: cat, amount: amt }}]);
                document.getElementById('expAmt').value = '';
            }}
            refreshUI();
        }}
    </script>
</body>
</html>
"""

components.html(html_code, height=1200, scrolling=True)