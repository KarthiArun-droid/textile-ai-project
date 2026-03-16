"use client"

import { BarChart3, Camera, Cpu, Activity } from "lucide-react"

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-slate-950 text-white flex">

      {/* Sidebar */}
      <div className="w-64 bg-slate-900 p-6">

        <h1 className="text-2xl font-bold mb-10">
          TextileMind AI
        </h1>

        <div className="space-y-6">

          <div className="flex gap-3 items-center">
            <BarChart3 size={18}/>
            Dashboard
          </div>

          <div className="flex gap-3 items-center">
            <Camera size={18}/>
            Cameras
          </div>

          <div className="flex gap-3 items-center">
            <Cpu size={18}/>
            AI Monitor
          </div>

          <div className="flex gap-3 items-center">
            <Activity size={18}/>
            Analytics
          </div>

        </div>

      </div>


      {/* Main Dashboard */}

      <div className="flex-1 p-10">

        <h2 className="text-3xl font-bold mb-10">
          Factory AI Control Center
        </h2>


        {/* Stats */}

        <div className="grid grid-cols-4 gap-6">

          <div className="bg-slate-800 p-6 rounded-xl">
            <p className="text-gray-400">Machines Running</p>
            <h3 className="text-2xl font-bold">24</h3>
          </div>

          <div className="bg-slate-800 p-6 rounded-xl">
            <p className="text-gray-400">Defects Today</p>
            <h3 className="text-2xl font-bold">43</h3>
          </div>

          <div className="bg-slate-800 p-6 rounded-xl">
            <p className="text-gray-400">AI Accuracy</p>
            <h3 className="text-2xl font-bold">97.3%</h3>
          </div>

          <div className="bg-slate-800 p-6 rounded-xl">
            <p className="text-gray-400">Production Rate</p>
            <h3 className="text-2xl font-bold">1320 m/hr</h3>
          </div>

        </div>


        {/* Camera Panel */}

        <div className="mt-10 bg-slate-800 p-6 rounded-xl">

          <h3 className="text-xl mb-4">
            Live Fabric Inspection
          </h3>

          <div className="bg-black h-64 rounded-lg flex items-center justify-center">

            Camera Feed

          </div>

        </div>

      </div>

    </div>
  )
}